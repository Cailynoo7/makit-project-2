# cell: star
import math
star_surface_shift=param("star_surface_shift",5.0)
star_outer_radius=param("star_outer_radius",32.0)
star_inner_radius=param("star_inner_radius",18.0)
star_center_z=param("star_center_z",104.0)
star_depth=param("star_depth",3.0)
star_corner_radius=param("star_corner_radius",1.6)
star_outline_width=param("star_outline_width",1.7)
star_eye_radius=param("star_eye_radius",3.2)
star_outline_depth=param("star_outline_depth",0.8)
star_body_edge_radius=param("star_body_edge_radius",1.2)
star_face_eye_height_radius=param("star_face_eye_height_radius",4.3)
star_face_eye_spacing=param("star_face_eye_spacing",20.0)
star_face_eye_z=param("star_face_eye_z",106.0)
star_face_depth=param("star_face_depth",1.2)
star_face_eye_edge_radius=param("star_face_eye_edge_radius",0.5)
star_face_mouth_z=param("star_face_mouth_z",99.5)
star_face_mouth_span=param("star_face_mouth_span",9.0)
star_face_mouth_dip=param("star_face_mouth_dip",2.2)
star_face_mouth_width=param("star_face_mouth_width",0.9)
star_face_mouth_edge_radius=param("star_face_mouth_edge_radius",0.35)
def left(s,d=69):
 return Rot(0,0,270)*Pos(0,-(d+star_surface_shift),0)*Rot(90,0,0)*s
def rolled(profile,depth,r):
 blank=extrude(profile,amount=depth,dir=(0,0,1))
 return fillet(blank.edges().group_by(Axis.Z)[-1],radius=r)
def star_sketch(ro,ri):
 # One repeated 72-degree sector guarantees five identical outer tips.
 pts=[]
 for i in range(10):
  angle=math.radians(90+i*36)
  radius=ro if i%2==0 else ri
  pts.append((radius*math.cos(angle),radius*math.sin(angle)))
 return fillet(Polygon(*pts,align=None).vertices(),radius=star_corner_radius)
body_profile=star_sketch(star_outer_radius,star_inner_radius)
outline_profile=offset(body_profile,amount=star_outline_width)
outline=left(Pos(0,star_center_z,0)*extrude(outline_profile,amount=star_outline_depth,dir=(0,0,1)))
outline.color=Color(1.0,0.61,0.04)
publish("star_outline",outline,"Fine golden star edge",material="pla")
body_blank=rolled(body_profile,star_depth,star_body_edge_radius)
body=left(Pos(0,star_center_z,0)*body_blank,69+star_outline_depth)
body.color=Color(1.0,0.77,0.06)
publish("star_body",body,"Soft rounded yellow star",material="pla")
front=69+star_outline_depth+star_depth
features=[]
for x in (-star_face_eye_spacing/2,star_face_eye_spacing/2):
 features.append(left(Pos(x,star_face_eye_z,0)*rolled(Ellipse(star_eye_radius,star_face_eye_height_radius),star_face_depth,star_face_eye_edge_radius),front))
# Round ended constant-width smile arc.
half=star_face_mouth_span/2
sag=star_face_mouth_dip
radius=(half*half+sag*sag)/(2*sag)
centre_y=star_face_mouth_z+radius-sag
angle=math.degrees(math.asin(half/radius))
outer=CenterArc((0,centre_y),radius+star_face_mouth_width/2,-90-angle,2*angle)
inner=CenterArc((0,centre_y),radius-star_face_mouth_width/2,-90-angle,2*angle)
wire=Wire([outer,Edge.make_line(outer@1,inner@1),inner.reversed(),Edge.make_line(inner@0,outer@0)])
mouth=extrude(Face(wire),amount=star_face_depth,dir=(0,0,1))
for x in (-half,half):
 mouth=mouth+Pos(x,star_face_mouth_z,0)*extrude(Circle(star_face_mouth_width/2),amount=star_face_depth)
mouth=fillet(mouth.edges().group_by(Axis.Z)[-1],radius=star_face_mouth_edge_radius)
features.append(left(mouth,front))
dark=Compound(children=features)
dark.color=Color(0.27,0.12,0.08)
publish("star_face",dark,"Oval eyes and fine smile",material="pla")
# Confetti centres from reference, adjustable individually in the star frame.
groups=[
 ("star_sprinkles","Blue confetti",Color(.1,.62,.88),[("upper_left",-30.55,26.76),("lower_left",-45.09,1.75),("upper_right",32.29,26.76)]),
 ("star_pink_confetti","Pink confetti",Color(1,.43,.66),[("upper_left",-41.02,19.78),("lower_left",-43.05,-25.31),("right",45.09,11.05)]),
 ("star_gold_confetti","Yellow confetti",Color(1,.75,.04),[("left",-38.98,-11.35),("right",42.18,-25.31)]),
 ("star_green_confetti","Green confetti",Color(.38,.76,.22),[("right",43.35,-6.11)])]
for oid,label,color,positions in groups:
 r=param(oid+"_radius",1.9)
 depth=param(oid+"_depth",1.4)
 edge_r=param(oid+"_edge_radius",0.5)
 dots=[]
 for key,px,pz in positions:
  x=param(oid+"_"+key+"_x",px)
  z=param(oid+"_"+key+"_z_offset",pz)
  dots.append(left(Pos(x,star_center_z+z,0)*rolled(Circle(r),depth,edge_r)))
 shape=Compound(children=dots) if len(dots)>1 else dots[0]
 shape.color=color
 publish(oid,shape,label,material="pla")
