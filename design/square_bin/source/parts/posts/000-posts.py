# cell: posts
import math
# cell: posts
# cell: posts
post_width=param("post_width",18.0)
post_bottom=param("post_bottom",43.0)
post_top=param("post_top",148.0)
blue_posts_guard_extension=param("blue_posts_guard_extension",8.0)
post_top=post_top-blue_posts_guard_extension
post_offset=param("post_offset",66.0)
post_host_width=param("post_host_width",150.0)
post_host_radius=param("post_host_radius",18.0)
post_insert_depth=param("post_insert_depth",4.0)
post_groove_width=param("post_groove_width",1.6)
post_groove_depth=param("post_groove_depth",0.75)
post_outward_growth=param("post_outward_growth",1.0)
post_host_width=post_host_width+2*post_outward_growth
post_host_radius=post_host_radius+post_outward_growth
post_insert_depth=post_insert_depth+post_outward_growth
post_width=post_width+post_outward_growth
post_offset=post_offset+post_outward_growth/2
outer_profile=RectangleRounded(post_host_width,post_host_width,post_host_radius)
inner_profile=RectangleRounded(post_host_width-2*post_insert_depth,post_host_width-2*post_insert_depth,post_host_radius-post_insert_depth)
band=Pos(0,0,post_bottom)*extrude(outer_profile-inner_profile,amount=post_top-post_bottom)
post_arc_angle_deg=param("post_arc_angle_deg",45.0)
corner_center=post_host_width/2-post_host_radius
a0=math.radians(45-post_arc_angle_deg/2)
a1=math.radians(45+post_arc_angle_deg/2)
reach=2*post_host_radius
wedge_profile=Polygon((corner_center,corner_center),(corner_center+reach*math.cos(a0),corner_center+reach*math.sin(a0)),(corner_center+reach*math.cos(a1),corner_center+reach*math.sin(a1)),align=None)
wedge=Pos(0,0,post_bottom)*extrude(wedge_profile,amount=post_top-post_bottom)
window=Pos(post_offset,post_offset,(post_bottom+post_top)/2)*Box(post_width,post_width,post_top-post_bottom)
one_corner=band & wedge & window
post_contact_radius=param("post_contact_radius",1.0)
one_corner=fillet(one_corner.edges(),radius=post_contact_radius)
posts=[Rot(0,0,rotation)*one_corner for rotation in (0,90,180,270)]
blue=Compound(children=posts)
# Continue the existing V grooves across the blue/cream tangent boundary.
groove_offset=post_host_width/2-post_host_radius
for rotation in (0,90,180,270):
 for x in (-groove_offset,groove_offset):
  section=Polygon((-post_groove_width/2,0),(post_groove_width/2,0),(0,post_groove_depth),align=None)
  cut=Rot(0,0,rotation)*Pos(x,-post_host_width/2,post_bottom)*extrude(section,amount=post_top-post_bottom)
  blue=blue-cut
blue.color=Color(0.08,0.49,0.83)
publish("blue_posts",blue,"Inset blue corner strips",material="pla")
