"""Generate open midsurfaces in millimetres; no solid wall or shell thickness in CAD.
Requires cadquery-ocp, numpy, scipy. Run with Python 3.
"""
from pathlib import Path
import json, math
import numpy as np
from scipy.interpolate import make_interp_spline
from OCP.gp import gp_Pnt, gp_Ax3, gp_Dir
from OCP.Geom import Geom_BSplineSurface, Geom_CylindricalSurface
try:
    from OCP.TColgp import TColgp_Array2OfPnt
    from OCP.TColStd import TColStd_Array1OfReal, TColStd_Array1OfInteger
except ImportError:
    from OCP.collections import Array2_gp_Pnt as TColgp_Array2OfPnt
    from OCP.collections import Array1_double as TColStd_Array1OfReal
    from OCP.collections import Array1_int as TColStd_Array1OfInteger
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_Sewing
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRep import BRep_Tool
from OCP.BRepTools import BRepTools
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE, TopAbs_SOLID, TopAbs_WIRE
from OCP.TopoDS import TopoDS
from OCP.ShapeAnalysis import ShapeAnalysis_FreeBounds
from OCP.STEPControl import STEPControl_Writer, STEPControl_Reader, STEPControl_AsIs
from OCP.IFSelect import IFSelect_RetDone

ROOT = Path(__file__).resolve().parents[2]
TOL = 1e-5

def array(values, cls):
    a = cls(1, len(values))
    for i, x in enumerate(values, 1): a.SetValue(i, x.item() if hasattr(x, 'item') else x)
    return a

def count(shape, kind):
    e = TopExp_Explorer(shape, kind); n = 0
    while e.More(): n += 1; e.Next()
    return n

def surface(depth, width):
    if depth == 0:
        return Geom_CylindricalSurface(gp_Ax3(gp_Pnt(0,0,0), gp_Dir(0,0,1)),75), (0,2*math.pi,0,450)
    u = np.linspace(-math.pi,math.pi,257)
    v = np.linspace(0,450,181)
    U,V = np.meshgrid(u,v,indexing='ij')
    R = 75-depth*np.exp(-0.5*((V-225)/width)**2-0.5*(75*U/width)**2)
    xyz = np.stack((R*np.cos(U),R*np.sin(U),V),axis=-1)
    su = make_interp_spline(u,xyz,k=5,axis=0)
    sv = make_interp_spline(v,su.c,k=5,axis=1)
    poles = np.moveaxis(sv.c,0,1)
    pp = TColgp_Array2OfPnt(1,poles.shape[0],1,poles.shape[1])
    for i in range(poles.shape[0]):
        for j in range(poles.shape[1]): pp.SetValue(i+1,j+1,gp_Pnt(*poles[i,j]))
    uk,um = np.unique(su.t,return_counts=True); vk,vm = np.unique(sv.t,return_counts=True)
    s = Geom_BSplineSurface(pp,array(uk,TColStd_Array1OfReal),array(vk,TColStd_Array1OfReal),array(um,TColStd_Array1OfInteger),array(vm,TColStd_Array1OfInteger),5,5)
    return s, (-math.pi,math.pi,0,450)

def generate(name, depth, width):
    s,b = surface(depth,width)
    face = BRepBuilderAPI_MakeFace(s,*b,1e-7).Face()
    sewing = BRepBuilderAPI_Sewing(1e-6); sewing.Add(face); sewing.Perform()
    shape = sewing.SewedShape()
    assert BRepCheck_Analyzer(shape).IsValid()
    path = ROOT/'geometry'/name; path.parent.mkdir(parents=True,exist_ok=True)
    writer=STEPControl_Writer(); writer.Transfer(shape,STEPControl_AsIs)
    assert writer.Write(str(path)) == IFSelect_RetDone
    reader=STEPControl_Reader(); assert reader.ReadFile(str(path)) == IFSelect_RetDone
    reader.TransferRoots(); imported=reader.OneShape()
    assert BRepCheck_Analyzer(imported).IsValid()
    assert count(imported,TopAbs_SOLID)==0 and count(imported,TopAbs_FACE)==1
    free=ShapeAnalysis_FreeBounds(imported,1e-6,False,True)
    closed=count(free.GetClosedWires(),TopAbs_WIRE); opened=count(free.GetOpenWires(),TopAbs_WIRE)
    assert closed==2 and opened==0, (closed,opened)
    ex=TopExp_Explorer(imported,TopAbs_FACE)
    cast=getattr(TopoDS,'Face_s',None) or TopoDS.Face
    imported_face=cast(ex.Current())
    surf=BRep_Tool.Surface_s(imported_face)
    error=0.; center=None; minrad=100.; maxrad=0.
    # Reimported surface is sampled against the analytical radial definition.
    ub=BRepTools.UVBounds_s(imported_face)
    for uu in np.linspace(ub[0],ub[1],193):
        for vv in np.linspace(ub[2],ub[3],137):
            p=surf.Value(float(uu),float(vv)); rad=math.hypot(p.X(),p.Y())
            theta=math.atan2(p.Y(),p.X())
            target=75-depth*math.exp(-.5*((p.Z()-225)/width)**2-.5*(75*theta/width)**2)
            error=max(error,abs(rad-target)); minrad=min(minrad,rad); maxrad=max(maxrad,rad)
    p=s.Value(0,225); center=math.hypot(p.X(),p.Y())
    assert error<TOL and abs(center-(75-depth))<TOL
    report=dict(file=str(path.relative_to(ROOT)),depth_mm=depth,width_mm=width,
                radius_mm=75,length_mm=450,shell_thickness_to_assign_mm=.4,
                center_radius_mm=center,max_sampled_radial_error_mm=error,
                tolerance_mm=TOL,valid_after_step_reimport=True,faces=1,solids=0,
                closed_free_rims=closed,open_free_wires=opened,
                notes='BRep validity, topology and sampled surface checks passed; Mechanical import still required.')
    print(json.dumps(report)); return report

if __name__=='__main__':
    reports=[generate('perfect_cylinder.step',0,20),generate('gaussian_baseline.step',.04,20)]
    (ROOT/'verification'/'geometry.json').write_text(json.dumps(reports,indent=2))
