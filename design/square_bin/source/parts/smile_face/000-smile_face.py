# cell: smile_face
import math
smile_face_surface_shift=param("smile_face_surface_shift",5.0)
face_width=param("face_width",84.0)
face_height=param("face_height",74.0)
face_center_z=param("face_center_z",105.0)
face_relief=param("face_relief",2.4)
face_panel_relief=param("face_panel_relief",2.0)
face_edge_radius=param("face_edge_radius",0.8)
eye_spacing=param("eye_spacing",44.0)
face_eye_z=param("face_eye_z",99.0)
cheek_radius=param("cheek_radius",5.2)
face_border_corner_radius=param("face_border_corner_radius",10.0)
face_panel_inset=param("face_panel_inset",3.5)
face_features_heart_width=param("face_features_heart_width",15.3)
face_features_heart_height=param("face_features_heart_height",13.7)
face_features_eye_relief=param("face_features_eye_relief",1.5)
face_features_eye_edge_radius=param("face_features_eye_edge_radius",0.5)
face_features_mouth_width=param("face_features_mouth_width",10.4)
face_features_mouth_dip=param("face_features_mouth_dip",2.7)
face_features_mouth_end_z=param("face_features_mouth_end_z",93.5)
face_features_mouth_stroke=param("face_features_mouth_stroke",1.1)
face_features_mouth_relief=param("face_features_mouth_relief",1.1)
face_features_mouth_edge_radius=param("face_features_mouth_edge_radius",0.4)
face_cheeks_x=param("face_cheeks_x",26.2)
face_cheeks_z=param("face_cheeks_z",92.1)
face_cheeks_relief=param("face_cheeks_relief",1.3)
face_cheeks_edge_radius=param("face_cheeks_edge_radius",0.5)
face_pins_x=param("face_pins_x",30.0)
face_pins_z=param("face_pins_z",128.5)
face_pins_radius=param("face_pins_radius",4.4)
face_pins_relief=param("face_pins_relief",1.4)
face_pins_edge_radius=param("face_pins_edge_radius",0.5)
# Existing host surface 69 plus shift and the stored -6 mm assembly placement.
host_depth=69.0
feature_depth=host_depth+face_relief+face_panel_relief
def on_front(shape,depth):
 return Pos(0,-(depth+smile_face_surface_shift),0)*Rot(90,0,0)*shape
def raised(profile,thickness,edge_radius):
 s=extrude(profile,amount=thickness)
 return fillet(s.edges().group_by(Axis.Z)[-1],radius=edge_radius)
border_blank=raised(RectangleRounded(face_width,face_height,face_border_corner_radius),face_relief,face_edge_radius)
border=on_front(Pos(0,face_center_z,0)*border_blank,host_depth)
border.color=Color(1.0,0.64,0.02)
publish("face_border",border,"Rounded gold plaque rim",material="pla")
panel_blank=raised(RectangleRounded(face_width-2*face_panel_inset,face_height-2*face_panel_inset,face_border_corner_radius-face_panel_inset),face_panel_relief,face_edge_radius)
panel=on_front(Pos(0,face_center_z,0)*panel_blank,host_depth+face_relief)
panel.color=Color(1.0,0.76,0.17)
publish("face_panel",panel,"Soft yellow face plaque",material="pla")
# Smooth cubic lobes, a narrow cleft, and a rounded bottom tip traced from the frontal reference.
face_features_heart_fullness=param("face_features_heart_fullness",0.08)
f=face_features_heart_fullness
control=[
 [(0,.24+f/2),(-.20,.58+f),(-.50,.57+f/2),(-.50,.18)],
 [(-.50,.18),(-.50,-.10),(-.20,-.37),(-.055,-.47)],
 [(-.055,-.47),(-.025,-.495),(.025,-.495),(.055,-.47)],
 [(.055,-.47),(.20,-.37),(.50,-.10),(.50,.18)],
 [(.50,.18),(.50,.57+f/2),(.20,.58+f),(0,.24+f/2)]]
unit_edges=[Bezier(*points) for points in control]
unit_wire=Wire(unit_edges)
bounds=unit_wire.bounding_box()
mid_y=(bounds.min.Y+bounds.max.Y)/2
sx=face_features_heart_width/bounds.size.X
sy=face_features_heart_height/bounds.size.Y
edges=[Bezier(*[(x*sx,(y-mid_y)*sy) for x,y in points]) for points in control]
heart_profile=Face(Wire(edges))
heart=raised(heart_profile,face_features_eye_relief,face_features_eye_edge_radius)
features=[]
for x in (-eye_spacing/2,eye_spacing/2):
 features.append(on_front(Pos(x,face_eye_z,0)*heart,feature_depth))
# A constant-width circular smile with rounded ends, instead of a broad crescent.
half=face_features_mouth_width/2
dip=face_features_mouth_dip
radius=(half*half+dip*dip)/(2*dip)
cy=face_features_mouth_end_z+radius-dip
stroke=face_features_mouth_stroke
theta=math.atan2(half,radius-dip)
reach=(radius+stroke)/math.cos(theta)
sector=Polygon((0,cy),(-reach*math.sin(theta),cy-reach*math.cos(theta)),(reach*math.sin(theta),cy-reach*math.cos(theta)),align=None)
mouth=(Pos(0,cy)*(Circle(radius+stroke/2)-Circle(radius-stroke/2))) & sector
for x in (-half,half):
 mouth=mouth+(Pos(x,face_features_mouth_end_z)*Circle(stroke/2))
mouth=raised(mouth,face_features_mouth_relief,face_features_mouth_edge_radius)
features.append(on_front(mouth,feature_depth))
dark=Compound(children=features)
assert len(dark.solids())==3, f'Expected two eyes and one mouth, got {len(dark.solids())}'
dark.color=Color(0.31,0.11,0.09)
publish("face_features",dark,"Rounded heart eyes and smile",material="pla")
cheek=raised(Circle(cheek_radius),face_cheeks_relief,face_cheeks_edge_radius)
cheeks=[on_front(Pos(x,face_cheeks_z,0)*cheek,feature_depth) for x in (-face_cheeks_x,face_cheeks_x)]
pink=Compound(children=cheeks)
pink.color=Color(1.0,0.46,0.64)
publish("face_cheeks",pink,"Round pink cheeks",material="pla")
pin=raised(Circle(face_pins_radius),face_pins_relief,face_pins_edge_radius)
left_pin=on_front(Pos(-face_pins_x,face_pins_z,0)*pin,feature_depth)
left_pin.color=Color(0.03,0.65,0.83)
publish("face_blue_pin",left_pin,"Blue plaque pin",material="pla")
right_pin=on_front(Pos(face_pins_x,face_pins_z,0)*pin,feature_depth)
right_pin.color=Color(1.0,0.42,0.02)
publish("face_orange_pin",right_pin,"Orange plaque pin",material="pla")
