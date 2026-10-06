import math
mushroom_surface_shift=param("mushroom_surface_shift",5.0)
mushroom_width=param("mushroom_width",70.0)
mushroom_center_z=param("mushroom_center_z",109.0)
mushroom_depth=param("mushroom_depth",3.0)
mushroom_cap_crown_lift=param("mushroom_cap_crown_lift",2.0)
mushroom_edge_radius=param("mushroom_edge_radius",0.8)
mushroom_cap_inner_edge_radius=param("mushroom_cap_inner_edge_radius",0.8)
mushroom_outline=param("mushroom_outline",2.0)
mushroom_stem_width=param("mushroom_stem_width",27.0)
mushroom_star_radius=param("mushroom_star_radius",7.0)
mushroom_cap_outline_depth=param("mushroom_cap_outline_depth",1.0)
mushroom_cap_outline_edge_radius=param("mushroom_cap_outline_edge_radius",0.5)
mushroom_stem_height=param("mushroom_stem_height",22.0)
mushroom_stem_z=param("mushroom_stem_z",81.6)
mushroom_stem_depth=param("mushroom_stem_depth",2.4)
mushroom_stem_edge_radius=param("mushroom_stem_edge_radius",1.0)
mushroom_gill_width=param("mushroom_gill_width",53.8)
mushroom_gill_height=param("mushroom_gill_height",8.0)
mushroom_gill_z=param("mushroom_gill_z",92.9)
mushroom_gill_depth=param("mushroom_gill_depth",1.2)
mushroom_gill_edge_radius=param("mushroom_gill_edge_radius",0.5)
mushroom_spots_depth=param("mushroom_spots_depth",1.2)
mushroom_spots_edge_radius=param("mushroom_spots_edge_radius",0.5)
mushroom_stars_depth=param("mushroom_stars_depth",1.5)
mushroom_stars_corner_radius=param("mushroom_stars_corner_radius",1.1)
mushroom_stars_edge_radius=param("mushroom_stars_edge_radius",0.6)
def back(s,d=69):
 return Rot(0,0,180)*Pos(0,-(d+mushroom_surface_shift),0)*Rot(90,0,0)*s
def rolled(profile,depth,r):
 s=extrude(profile,amount=depth,dir=(0,0,1))
 return fillet(s.edges().group_by(Axis.Z)[-1],radius=r)
# Cubic curves traced from the lower-left reference panel.
# Reference cap centre=(399,1150), nominal cap width226 pixels.
cap_curves=[
 [(286,1170),(291,1111),(343,1073),(399,1073)],
 [(399,1073),(457,1073),(509,1111),(513,1170)],
 [(513,1170),(530,1210),(459,1220),(399,1220)],
 [(399,1220),(340,1220),(270,1210),(286,1170)]]
scale=mushroom_width/226
cap_profile=Face(Wire([Bezier(*[((x-399)*scale,mushroom_center_z+(1150-y)*scale+mushroom_cap_crown_lift*max((1150-y)/77,0)) for x,y in pts]) for pts in cap_curves]))
stem_curves=[
 [(-.43,.46),(-.23,.51),(.23,.51),(.43,.46)],
 [(.43,.46),(.426,.19),(.49,-.07),(.5,-.26)],
 [(.5,-.26),(.51,-.44),(.29,-.5),(0,-.5)],
 [(0,-.5),(-.29,-.5),(-.51,-.44),(-.5,-.26)],
 [(-.5,-.26),(-.49,-.07),(-.426,.19),(-.43,.46)]]
stem_profile=Face(Wire([Bezier(*[(x*mushroom_stem_width,mushroom_stem_z+y*mushroom_stem_height) for x,y in pts]) for pts in stem_curves]))
gill_profile=Pos(0,mushroom_gill_z)*Ellipse(mushroom_gill_width/2,mushroom_gill_height/2)
cap_pink_profile=Face(Wire([Bezier(*[((x-399)*scale*(1+2*mushroom_outline/mushroom_width),mushroom_center_z+((1150-y)*scale+mushroom_cap_crown_lift*max((1150-y)/77,0))*(1+2*mushroom_outline/(147*scale))) for x,y in pts]) for pts in cap_curves]))
cap_pink_blank=rolled(cap_pink_profile,mushroom_cap_outline_depth,mushroom_cap_outline_edge_radius)
stem_pink_profile=Face(Wire([Bezier(*[(x*(mushroom_stem_width+2*mushroom_outline),mushroom_stem_z+y*(mushroom_stem_height+2*mushroom_outline)) for x,y in pts]) for pts in stem_curves]))
stem_pink_blank=rolled(stem_pink_profile-cap_pink_profile,mushroom_cap_outline_depth,mushroom_cap_outline_edge_radius)
cap_pink=back(cap_pink_blank)
cap_pink.color=Color(1,.49,.68)
publish("mushroom_cap_outline",cap_pink,"Rounded pink cap outline",material="pla")
stem_pink=back(stem_pink_blank)
stem_pink.color=Color(1,.54,.71)
publish("mushroom_stem_border",stem_pink,"Rounded pink stem outline",material="pla")
cap_blank=rolled(cap_profile,mushroom_depth,mushroom_edge_radius)
cap_blank=cap_blank-extrude(gill_profile,amount=mushroom_depth)-extrude(stem_profile,amount=mushroom_depth,dir=(0,0,1))
inner_edges=cap_blank.edges().filter_by(GeomType.ELLIPSE).filter_by_position(Axis.Z,mushroom_depth-.00001,mushroom_depth+.00001)
assert len(inner_edges)>0
cap_blank=fillet(inner_edges,radius=mushroom_cap_inner_edge_radius)
gill_blank=Pos(0,0,mushroom_depth-mushroom_gill_depth)*rolled(gill_profile-stem_profile,mushroom_gill_depth,mushroom_gill_edge_radius)
stem_blank=rolled(stem_profile,mushroom_stem_depth,mushroom_stem_edge_radius)
assert cap_blank.is_valid and stem_blank.is_valid
cap=back(cap_blank,69+mushroom_cap_outline_depth)
cap.color=Color(.97,.13,.18)
publish("mushroom_cap",cap,"Smooth red mushroom cap",material="pla")
gill=back(gill_blank,69+mushroom_cap_outline_depth)
gill.color=Color(.99,.95,.82)
publish("mushroom_gill",gill,"Cream oval underside",material="pla")
stem=back(stem_blank,69+mushroom_cap_outline_depth)
stem.color=Color(1,.73,.08)
publish("mushroom_stem",stem,"Flared rounded yellow stem",material="pla")
spots=[]
for key,px,pz,rx,rz,angle in [("left",-27.0,110.5,4.8,7.1,-18),("centre",.9,117.4,11.3,10.4,0),("right",27.0,110.5,4.8,7.1,18)]:
 x=param("mushroom_spots_"+key+"_x",px)
 z=param("mushroom_spots_"+key+"_z",pz)
 r1=param("mushroom_spots_"+key+"_radius_x",rx)
 r2=param("mushroom_spots_"+key+"_radius_z",rz)
 tilt=param("mushroom_spots_"+key+"_tilt",angle)
 spots.append(back(Pos(x,z)*Rot(0,0,tilt)*rolled(Ellipse(r1,r2),mushroom_spots_depth,mushroom_spots_edge_radius),69+mushroom_cap_outline_depth+mushroom_depth))
white=Compound(children=spots)
white.color=Color(1,1,1)
publish("mushroom_spots",white,"Three rounded white spots",material="pla")
stars=[]
for key,px,pz,factor in [("left",-40.6,135.6,1),("right",36.9,136.9,.73)]:
 x=param("mushroom_stars_"+key+"_x",px)
 z=param("mushroom_stars_"+key+"_z",pz)
 ro=mushroom_star_radius*factor
 pts=[((ro if i%2==0 else ro*.5)*math.cos(math.radians(90+i*36)),(ro if i%2==0 else ro*.5)*math.sin(math.radians(90+i*36))) for i in range(10)]
 profile=fillet(Polygon(*pts,align=None).vertices(),radius=mushroom_stars_corner_radius*factor)
 stars.append(back(Pos(x,z)*rolled(profile,mushroom_stars_depth,mushroom_stars_edge_radius)))
gold=Compound(children=stars)
gold.color=Color(1,.77,.02)
publish("mushroom_stars",gold,"Two soft yellow stars",material="pla")
blue_depth=param("mushroom_blue_dots_depth",1.5)
blue_edge=param("mushroom_blue_dots_edge_radius",.45)
blue_upper_edge=param("mushroom_blue_dots_upper_small_edge_radius",.8)
dots=[]
for key,px,pz,r0 in [("lower_left",-42.1,76.2,2.3),("lower_small",-29.7,70.6,1.3),("upper_small",-17.0,144.0,.9)]:
 x=param("mushroom_blue_dots_"+key+"_x",px)
 z=param("mushroom_blue_dots_"+key+"_z",pz)
 r=param("mushroom_blue_dots_"+key+"_radius",r0)
 dots.append(back(Pos(x,z)*rolled(Circle(r),blue_depth,blue_upper_edge if key=="upper_small" else blue_edge)))
blue=Compound(children=dots)
blue.color=Color(.04,.65,.88)
publish("mushroom_blue_dots",blue,"Three rounded blue dots",material="pla")
ox=param("mushroom_orange_dot_x",40.9)
oz=param("mushroom_orange_dot_z",77.7)
orr=param("mushroom_orange_dot_radius",2.3)
od=param("mushroom_orange_dot_depth",1.5)
oe=param("mushroom_orange_dot_edge_radius",.5)
orange=back(Pos(ox,oz)*rolled(Circle(orr),od,oe))
orange.color=Color(1,.57,.04)
publish("mushroom_orange_dot",orange,"Rounded orange dot",material="pla")
