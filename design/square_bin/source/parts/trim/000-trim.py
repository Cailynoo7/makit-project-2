# cell: trim
import math
trim_outer=param("trim_outer",162.0)
trim_inner=param("trim_inner",150.0)
trim_z=param("trim_z",35.0)
trim_height=param("trim_height",8.0)
scallop_radius=param("scallop_radius",9.5)
scallop_pitch=param("scallop_pitch",16.0)
trim_edge_radius=param("trim_edge_radius",0.8)
trim_outer_corner_radius=param("trim_outer_corner_radius",24.0)
trim_inner_corner_radius=param("trim_inner_corner_radius",18.0)
trim_waves_per_side=param("trim_waves_per_side",9)
trim_scallop_drop=param("trim_scallop_drop",5.5)
trim_base_fit_width=param("trim_base_fit_width",160.0)
trim_base_fit_radius=param("trim_base_fit_radius",23.0)
trim_base_fit_top=param("trim_base_fit_top",35.0)
assert int(trim_waves_per_side)==trim_waves_per_side
profile=RectangleRounded(trim_outer,trim_outer,trim_outer_corner_radius)-RectangleRounded(trim_inner,trim_inner,trim_inner_corner_radius)
band=Pos(0,0,trim_z)*extrude(profile,amount=trim_height)
low=trim_z-trim_scallop_drop
mask=Pos(0,0,low)*extrude(profile,amount=trim_height+trim_scallop_drop)
half=trim_outer/2
r=trim_outer_corner_radius
corner=half-r
arc=math.pi*r/2
perimeter=8*corner+4*arc
count=int(4*trim_waves_per_side)
pitch=perimeter/count
assert scallop_radius>pitch/2, "Wave arcs must overlap continuously around the perimeter"
def station(s):
 segments=[
  ("line",corner,(0,-half),(1,0),(0,-1)),
  ("arc",arc,(corner,-corner),-math.pi/2,None),
  ("line",2*corner,(half,-corner),(0,1),(1,0)),
  ("arc",arc,(corner,corner),0,None),
  ("line",2*corner,(corner,half),(-1,0),(0,1)),
  ("arc",arc,(-corner,corner),math.pi/2,None),
  ("line",2*corner,(-half,corner),(0,-1),(-1,0)),
  ("arc",arc,(-corner,-corner),math.pi,None),
  ("line",corner,(-corner,-half),(1,0),(0,-1))]
 for kind,length,start,direction,normal in segments:
  if s<=length+1e-8:
   if kind=="line":
    return (start[0]+direction[0]*s,start[1]+direction[1]*s),normal
   angle=direction+s/r
   normal=(math.cos(angle),math.sin(angle))
   return (start[0]+r*normal[0],start[1]+r*normal[1]),normal
  s-=length
 raise ValueError("Perimeter station out of range")
wall=(trim_outer-trim_inner)/2
waves=[]
for i in range(count):
 (x,y),(nx,ny)=station((i+0.5)*pitch)
 plane=Plane(origin=(x-nx*(wall+2),y-ny*(wall+2),low+scallop_radius),z_dir=(nx,ny,0))
 waves.append(plane*Cylinder(scallop_radius,wall+4,align=(Align.CENTER,Align.CENTER,Align.MIN)))
wave_union=waves[0].fuse(*waves[1:])
green=band+(wave_union & mask)
# Round lower perimeter and wave junctions while the full ring thickness supports the blend.
green_trim_lower_edge_radius=param("green_trim_lower_edge_radius",0.4)
lower_edges=[e for e in green.edges() if e.bounding_box().max.Z<trim_z+0.001]
assert len(lower_edges)>0
green=fillet(lower_edges,radius=green_trim_lower_edge_radius)
base_fit=extrude(RectangleRounded(trim_base_fit_width,trim_base_fit_width,trim_base_fit_radius),amount=trim_base_fit_top)
green=green-base_fit
top_edges=[e for e in green.edges() if abs(e.center().Z-(trim_z+trim_height))<0.001]
green=fillet(top_edges,radius=trim_edge_radius)
assert len(green.solids())==1, "Trim must be one uninterrupted closed ring"
print("Closed wave ring:",count,"waves; effective pitch",pitch,"mm")
green.color=Color(0.29,0.69,0.25)
publish("green_trim",green,"Continuous scalloped trim",material="pla")
