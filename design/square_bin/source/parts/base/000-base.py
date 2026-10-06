# cell: base
# cell: base
import math
# cell: base
# cell: base
base_width=param("base_width",146.0)
base_height=param("base_height",35.0)
base_opening=param("base_opening",138.0)
base_corner_radius=param("base_corner_radius",12.0)
base_outward_growth=param("base_outward_growth",1.0)
base_width=base_width+2*base_outward_growth
base_corner_radius=base_corner_radius+base_outward_growth
outer_profile=RectangleRounded(base_width,base_width,base_corner_radius)
base_body_nominal_width=param("base_body_nominal_width",145.0)
base_body_nominal_radius=param("base_body_nominal_radius",15.5)
base_body_clearance=param("base_body_clearance",0.2)
base_opening=base_body_nominal_width+2*base_body_clearance
inner_profile=RectangleRounded(base_opening,base_opening,base_body_nominal_radius+base_body_clearance)
base=extrude(outer_profile-inner_profile,amount=base_height)
# Three brick courses are carved into one continuous cladding ring.
base_brick_rows=param("base_brick_rows",3)
base_brick_pitch=param("base_brick_pitch",28.0)
base_joint_width=param("base_joint_width",1.2)
base_joint_depth=param("base_joint_depth",0.8)
base_joint_edge_radius=param("base_joint_edge_radius",0.25)
assert int(base_brick_rows)==base_brick_rows and base_brick_rows>=1
row_height=base_height/base_brick_rows
groove_inner=RectangleRounded(base_width-2*base_joint_depth,base_width-2*base_joint_depth,base_corner_radius-base_joint_depth)
joint_band=outer_profile-groove_inner
for i in range(1,int(base_brick_rows)):
 base=base-(Pos(0,0,i*row_height-base_joint_width/2)*extrude(joint_band,amount=base_joint_width))
corner_center=base_width/2-base_corner_radius
for row in range(int(base_brick_rows)):
 z0=row*row_height
 phase=base_brick_pitch/2 if row%2==0 else 0
 for n in range(-3,4):
  x=n*base_brick_pitch+phase
  if abs(x)+base_joint_width/2>=corner_center:
   continue
  for rotation in (0,90,180,270):
   cutter=Rot(0,0,rotation)*Pos(x,-base_width/2+base_joint_depth/2-0.01,z0+row_height/2)*Box(base_joint_width,base_joint_depth+0.02,row_height+base_joint_width)
   base=base-cutter
# Radius the brick outline in the face plane before rolling the exposed perimeter.
base_brick_outline_radius=param("base_brick_outline_radius",2.0)
corner_edges=[]
for e in base.edges():
 bb=e.bounding_box()
 if e.geom_type==GeomType.LINE and abs(e.length-base_joint_depth)<0.001 and bb.size.Z<0.001:
  if (abs(bb.size.X-base_joint_depth)<0.001 and bb.size.Y<0.001) or (abs(bb.size.Y-base_joint_depth)<0.001 and bb.size.X<0.001):
   corner_edges.append(e)
assert len(corner_edges)>0, "Brick outline corners must be selected"
base=fillet(corner_edges,radius=base_brick_outline_radius)
# Round all four exposed edges of each brick, including the uppermost and lowermost perimeter.
mouth=[]
for e in base.edges():
 c=e.center()
 r=math.hypot(max(abs(c.X)-corner_center,0),max(abs(c.Y)-corner_center,0))
 if abs(r-base_corner_radius)<0.001 and -0.001<=c.Z<=base_height+0.001:
  if e.geom_type==GeomType.CIRCLE or (e.geom_type==GeomType.LINE and (abs(c.X)<corner_center-0.01 or abs(c.Y)<corner_center-0.01)):
   mouth.append(e)
base=fillet(mouth,radius=base_joint_edge_radius)
base_grip_rib_width=param("base_grip_rib_width",6.0)
base_grip_rib_bottom=param("base_grip_rib_bottom",5.0)
base_grip_rib_top=param("base_grip_rib_top",30.0)
base_grip_interference=param("base_grip_interference",0.1)
base_grip_lead_height=param("base_grip_lead_height",2.0)
projection=base_body_clearance+base_grip_interference
half=base_opening/2
fuse_embed=0.05
rib_profile=Plane.YZ*Polygon(
 (-half-fuse_embed,base_grip_rib_bottom),
 (-half,base_grip_rib_bottom),
 (-half+projection,base_grip_rib_bottom+base_grip_lead_height),
 (-half+projection,base_grip_rib_top-base_grip_lead_height),
 (-half,base_grip_rib_top),
 (-half-fuse_embed,base_grip_rib_top),align=None)
rib=Pos(-base_grip_rib_width/2,0,0)*extrude(rib_profile,amount=base_grip_rib_width,dir=(1,0,0))
for rotation in (0,90,180,270):
 base=base+(Rot(0,0,rotation)*rib)
base_guard_depth=param("brown_base_guard_depth",4.0)
base_guard_clearance=param("brown_base_guard_clearance",0.2)
base_guard_height=param("brown_base_guard_height",22.0)
brown_base_guard_inward_growth=param("brown_base_guard_inward_growth",1.5)
base_guard_depth=base_guard_depth+brown_base_guard_inward_growth
seat_band=Pos(0,0,-base_guard_clearance)*extrude(outer_profile-RectangleRounded(base_width-2*(base_guard_depth+base_guard_clearance),base_width-2*(base_guard_depth+base_guard_clearance),base_corner_radius-base_guard_depth-base_guard_clearance),amount=base_guard_height+2*base_guard_clearance)
reach=base_corner_radius+base_guard_clearance
seat_mask=Pos(corner_center-base_guard_clearance+reach/2,corner_center-base_guard_clearance+reach/2,base_guard_height/2)*Box(reach,reach,base_guard_height+2*base_guard_clearance)
for rotation in (0,90,180,270):
 base=base-(seat_band & (Rot(0,0,rotation)*seat_mask))

assert len(base.solids())==1, "Brick cladding and grip ribs must remain one solid"
base.color=Color(0.62,0.35,0.20)
publish("brown_base",base,"Brown brick cladding",material="pla")
# Intended press fit: brown_base/shell, four local ribs, maximum0.1 mm; documented in README because fit metadata fails the current worker response schema.
