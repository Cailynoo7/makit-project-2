# cell: body
# cell: body
import math
# cell: body
# cell: body
# cell: body
# cell: body
# cell: body
# cell: body
# cell: body
# cell: body
bin_width = param("bin_width", 150.0)
bin_depth = param("bin_depth", 150.0)
bin_height = param("bin_height", 180.0)
shell_wall = param("shell_wall", 5.0)
shell_floor = param("shell_floor", 8.0)
body_width = param("body_width", 138.0)
body_bottom = param("body_bottom", 0.0)
body_top = param("body_top", 180.0)
outer_corner_radius = param("outer_corner_radius", 11.0)
floor_cove_radius = param("floor_cove_radius", 3.0)
# Base dimensions above are the preserved 1.1 values; growth controls are per side.
body_outward_growth=param("body_outward_growth",1.0)
body_inward_growth=param("body_inward_growth",1.0)
body_width=body_width+2*body_outward_growth
shell_wall=shell_wall+body_outward_growth+body_inward_growth
outer_corner_radius=outer_corner_radius+body_outward_growth
inner_corner_radius = outer_corner_radius-shell_wall
outer_profile = RectangleRounded(body_width, body_width, outer_corner_radius)
inner_profile = RectangleRounded(body_width-2*shell_wall, body_width-2*shell_wall, inner_corner_radius)
outer = Pos(0,0,body_bottom) * extrude(outer_profile, amount=body_top-body_bottom)
cavity = Pos(0,0,body_bottom+shell_floor) * extrude(inner_profile, amount=body_top-body_bottom)
shell = outer - cavity
floor_edges=[e for e in shell.edges() if abs(e.center().Z-(body_bottom+shell_floor))<0.01]
shell=fillet(floor_edges,radius=floor_cove_radius)
shell_tongue_height=param("shell_tongue_height",9.0)
tongue_outer=RectangleRounded(body_width-shell_wall,body_width-shell_wall,outer_corner_radius-shell_wall/2)
tongue=Pos(0,0,body_top)*extrude(tongue_outer-inner_profile,amount=shell_tongue_height)
shell=shell+tongue
shell_contact_radius=param("shell_contact_radius",1.0)
shell_inner_contact_radius=param("shell_inner_contact_radius",1.0)
outer_contact_edges=[e for e in shell.edges() if abs(e.center().Z-body_top)<0.001 and max(abs(e.bounding_box().min.X),abs(e.bounding_box().max.X),abs(e.bounding_box().min.Y),abs(e.bounding_box().max.Y))>body_width/2-0.01]
shell=fillet(outer_contact_edges,radius=shell_contact_radius)
inner_contact_edges=[e for e in shell.edges() if (abs(e.center().Z-body_top)<0.001 or abs(e.center().Z-(body_top+shell_tongue_height))<0.001) and max(abs(e.bounding_box().min.X),abs(e.bounding_box().max.X),abs(e.bounding_box().min.Y),abs(e.bounding_box().max.Y))<=(body_width-shell_wall)/2+0.01]
shell=fillet(inner_contact_edges,radius=shell_inner_contact_radius)
shell_groove_width=param("shell_groove_width",1.0)
shell_groove_depth=param("shell_groove_depth",0.6)
shell_groove_offset=param("shell_groove_offset",27.0)
shell_groove_bottom=param("shell_groove_bottom",43.0)
shell_groove_top=param("shell_groove_top",162.0)
shell_side_groove_offset=param("shell_side_groove_offset",57.0)
shell_side_groove_width=param("shell_side_groove_width",0.8)
shell_side_groove_depth=param("shell_side_groove_depth",0.5)
for rotation in (0,90,180,270):
 for x in (-shell_groove_offset,shell_groove_offset):
  section=Polygon((-shell_groove_width/2,0),(shell_groove_width/2,0),(0,shell_groove_depth),align=None)
  cutter=Rot(0,0,rotation)*Pos(x,-body_width/2,shell_groove_bottom)*extrude(section,amount=shell_groove_top-shell_groove_bottom)
  shell=shell-cutter
for rotation in (0,90,180,270):
 for x in (-shell_side_groove_offset,shell_side_groove_offset):
  section=Polygon((-shell_side_groove_width/2,0),(shell_side_groove_width/2,0),(0,shell_side_groove_depth),align=None)
  cutter=Rot(0,0,rotation)*Pos(x,-body_width/2,shell_groove_bottom)*extrude(section,amount=shell_groove_top-shell_groove_bottom)
  shell=shell-cutter
shell_corner_insert_depth=param("shell_corner_insert_depth",4.0)
shell_corner_insert_bottom=param("shell_corner_insert_bottom",43.0)
shell_corner_insert_top=param("shell_corner_insert_top",148.0)
cream_outer_shell_guard_extension=param("cream_outer_shell_guard_extension",8.0)
shell_corner_insert_top=shell_corner_insert_top-cream_outer_shell_guard_extension
shell_corner_insert_depth=shell_corner_insert_depth+body_outward_growth
pocket_inner=RectangleRounded(body_width-2*shell_corner_insert_depth,body_width-2*shell_corner_insert_depth,outer_corner_radius-shell_corner_insert_depth)
pocket_band=Pos(0,0,shell_corner_insert_bottom)*extrude(outer_profile-pocket_inner,amount=shell_corner_insert_top-shell_corner_insert_bottom)
shell_corner_insert_angle_deg=param("shell_corner_insert_angle_deg",45.0)
corner_center=body_width/2-outer_corner_radius
a0=math.radians(45-shell_corner_insert_angle_deg/2)
a1=math.radians(45+shell_corner_insert_angle_deg/2)
reach=2*outer_corner_radius
wedge_profile=Polygon((corner_center,corner_center),(corner_center+reach*math.cos(a0),corner_center+reach*math.sin(a0)),(corner_center+reach*math.cos(a1),corner_center+reach*math.sin(a1)),align=None)
wedge=Pos(0,0,shell_corner_insert_bottom)*extrude(wedge_profile,amount=shell_corner_insert_top-shell_corner_insert_bottom)
for rotation in (0,90,180,270):
 shell=shell-(pocket_band & (Rot(0,0,rotation)*wedge))
shell_corner_contact_radius=param("shell_corner_contact_radius",1.0)
interface_edges=[]
for e in shell.edges():
 c=e.center()
 r=math.hypot(abs(c.X)-corner_center,abs(c.Y)-corner_center)
 angle=math.degrees(math.atan2(abs(c.Y)-corner_center,abs(c.X)-corner_center))
 if 20<angle<70 and r>outer_corner_radius-shell_corner_insert_depth-0.1 and abs(c.X)>corner_center+0.01 and abs(c.Y)>corner_center+0.01 and shell_corner_insert_bottom-0.01<=c.Z<=shell_corner_insert_top+0.01:
  interface_edges.append(e)
assert len(interface_edges)==48, f"Expected 12 interface edges per corner, got {len(interface_edges)}"
shell=fillet(interface_edges,radius=shell_corner_contact_radius)
corner_backing=outer_corner_radius-shell_corner_insert_depth-inner_corner_radius
assert corner_backing>0, "Corner pocket must not reach the inner cavity"
print("Corner pocket backing wall:",corner_backing,"mm")
shell.color = Color(0.96,0.90,0.83)
# Split on the mid-wall offset; keep the continuous inner box and only the upper outer sleeve.
shell_outer_start_z=param("shell_outer_start_z",43.0)
inner_box_width=param("inner_box_width",145.0)
inner_box_depth=param("inner_box_depth",145.0)
inner_box_wall=param("inner_box_wall",6.5)
inner_box_top=param("inner_box_top",171.0)
inner_box_wall=inner_box_wall+body_inward_growth
split_radius=inner_corner_radius+inner_box_wall
mid_profile=RectangleRounded(inner_box_width,inner_box_depth,split_radius)
mid_volume=Pos(0,0,body_bottom)*extrude(mid_profile,amount=inner_box_top-body_bottom)
inner_box=shell & mid_volume
cream_outer_shell_clearance=param("cream_outer_shell_clearance",0.2)
sleeve_inner_profile=RectangleRounded(inner_box_width+2*cream_outer_shell_clearance,inner_box_depth+2*cream_outer_shell_clearance,split_radius+cream_outer_shell_clearance)
sleeve_inner_volume=Pos(0,0,body_bottom)*extrude(sleeve_inner_profile,amount=inner_box_top-body_bottom)
outer_layer=(shell-sleeve_inner_volume) & (Pos(0,0,shell_outer_start_z)*extrude(outer_profile,amount=body_top-shell_outer_start_z))
# Blind seats for upper flush guards; preserve continuous inner box.
shell_guard_depth=param("cream_outer_shell_guard_depth",4.0)
shell_guard_clearance=param("cream_outer_shell_guard_clearance",0.2)
shell_guard_bottom=param("cream_outer_shell_guard_bottom",148.0)
shell_guard_top=param("cream_outer_shell_guard_top",162.0)
cream_outer_shell_guard_inward_growth=param("cream_outer_shell_guard_inward_growth",1.5)
shell_guard_depth=shell_guard_depth+cream_outer_shell_guard_inward_growth
shell_guard_bottom=shell_guard_bottom-cream_outer_shell_guard_extension
seat_band=extrude(outer_profile-RectangleRounded(body_width-2*(shell_guard_depth+shell_guard_clearance),body_width-2*(shell_guard_depth+shell_guard_clearance),outer_corner_radius-shell_guard_depth-shell_guard_clearance),amount=shell_guard_top-shell_guard_bottom+2*shell_guard_clearance)
reach=outer_corner_radius+shell_guard_clearance
seat_mask=Pos(corner_center-shell_guard_clearance+reach/2,corner_center-shell_guard_clearance+reach/2,shell_guard_bottom-shell_guard_clearance+(shell_guard_top-shell_guard_bottom+2*shell_guard_clearance)/2)*Box(reach,reach,shell_guard_top-shell_guard_bottom+2*shell_guard_clearance)
for rotation in (0,90,180,270):
 outer_layer=outer_layer-(Pos(0,0,shell_guard_bottom-shell_guard_clearance)*seat_band & (Rot(0,0,rotation)*seat_mask))

assert len(inner_box.solids())==1 and len(outer_layer.solids())==1, "Each split piece must be one connected solid"
inner_box.color=Color(0.96,0.90,0.83)
outer_layer.color=Color(0.96,0.90,0.83)
publish("shell",inner_box,"Cream inner box",material="pla")
publish("cream_outer_shell",outer_layer,"Cream upper outer shell",material="pla")