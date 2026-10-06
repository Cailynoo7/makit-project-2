# cell: flower
# cell: flower
# cell: flower
# cell: flower
import math
flower_surface_shift=param("flower_surface_shift",5.0)
flower_radius=param("flower_radius",23.0)
petal_width=param("petal_width",24.0)
petal_height=param("petal_height",30.0)
flower_z=param("flower_z",105.0)
flower_depth=param("flower_depth",2.5)
flower_center_radius=param("flower_center_radius",10.0)
petal_edge_radius=param("petal_edge_radius",1.2)
flower_center_depth=param("flower_center_depth",1.8)
flower_center_edge_radius=param("flower_center_edge_radius",0.5)
flower_petals_root_web_margin=param("flower_petals_root_web_margin",3.0)
flower_center_socket_depth=param("flower_center_socket_depth",1.0)
flower_center_socket_clearance=param("flower_center_socket_clearance",0.2)
# Existing host datum and persisted +6 mm X placement put the backing at X80.
host_depth=69.0
def right(s,d):
 return Rot(0,0,90)*Pos(0,-(d+flower_surface_shift),0)*Rot(90,0,0)*s
# Control points traced from the upper-right flower in user reference image.
# Pixel coordinates are fixed reference proportions, scaled by the existing
# editable overall width/height and layout parameters. Centre=(1160,397);
# reference yellow disc radius=36 pixels.
scale=flower_center_radius/36
sx=scale*(petal_width/23)*(flower_radius/21)
sy=scale*(petal_height/28)*(flower_radius/21)
top=[
 [(1160,392),(1137,371),(1116,338),(1118,311)],
 [(1118,311),(1120,286),(1138,270),(1160,270)],
 [(1160,270),(1189,270),(1208,295),(1202,326)],
 [(1202,326),(1199,348),(1180,382),(1160,392)]]
# All five petals are rigid copies of the reference-traced upper petal.
profile=Face(Wire([Bezier(*[((x-1160)*sx,(397-y)*sy) for x,y in segment]) for segment in top]))
lobe=extrude(profile,amount=flower_depth,dir=(0,0,1))
lobe=fillet(lobe.edges().group_by(Axis.Z)[-1],radius=petal_edge_radius)
blank=extrude(Circle(flower_center_radius+flower_center_socket_clearance+flower_petals_root_web_margin),amount=flower_depth-flower_center_socket_depth)
for index in range(5):
 blank=blank+Rot(0,0,-index*360/5)*lobe
# Blind centre pocket; the continuous rear web connects all five lobes.
socket=Pos(0,0,flower_depth-flower_center_socket_depth)*extrude(Circle(flower_center_radius+flower_center_socket_clearance),amount=flower_center_socket_depth,dir=(0,0,1))
blank=blank-socket
assert len(blank.solids())==1 and blank.is_valid
white=right(Pos(0,flower_z,0)*blank,host_depth)
white.color=Color(0.98,0.96,0.97)
publish("flower_petals",white,"Single-piece five-petal flower",material="pla")
core_blank=extrude(Circle(flower_center_radius),amount=flower_center_depth,dir=(0,0,1))
core_blank=fillet(core_blank.edges().group_by(Axis.Z)[-1],radius=flower_center_edge_radius)
core=right(Pos(0,flower_z,0)*core_blank,host_depth+flower_depth-flower_center_socket_depth)
core.color=Color(1.0,0.72,0.05)
publish("flower_center",core,"Inset yellow flower centre",material="pla")
