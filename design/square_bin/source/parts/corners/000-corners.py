# cell: corners
# cell: corners
# Flush quarter-circle guards seated in blind pockets.
corner_offset=param("corner_offset",74.0)
corner_width=param("corner_width",14.0)
corner_lower_height=param("corner_lower_height",22.0)
corner_upper_z=param("corner_upper_z",148.0)
corner_upper_height=param("corner_upper_height",14.0)
corner_plan_radius=param("corner_plan_radius",4.0)
corner_edge_radius=param("corner_edge_radius",1.5)
corner_lower_fit_width=param("corner_lower_fit_width",160.0)
corner_lower_fit_radius=param("corner_lower_fit_radius",23.0)
corner_upper_host_width=param("corner_upper_host_width",158.0)
corner_upper_host_radius=param("corner_upper_host_radius",22.0)
corner_upper_outward_growth=param("corner_upper_outward_growth",1.0)
corner_guard_depth=param("pink_corners_depth",4.0)
corner_guard_seam_radius=param("pink_corners_seam_radius",0.6)
corner_guard_upper_top_radius=param("pink_corners_upper_top_radius",3.0)
pink_corners_inward_growth=param("pink_corners_inward_growth",1.5)
pink_corners_upper_extension=param("pink_corners_upper_extension",8.0)
corner_guard_depth=corner_guard_depth+pink_corners_inward_growth
corner_upper_z=corner_upper_z-pink_corners_upper_extension
corner_upper_height=corner_upper_height+pink_corners_upper_extension
# Upper guards share the lower guards' exposed edge radius.
corner_guard_upper_top_radius=corner_edge_radius
upper_width=corner_upper_host_width+2*corner_upper_outward_growth
upper_radius=corner_upper_host_radius+corner_upper_outward_growth
pink_corners_outward_growth=param("pink_corners_outward_growth",1.5)
def guard(r,depth,height,top_radius):
 # Increase the external radius and thickness equally; the rear radius and arc center stay fixed.
 r=r+pink_corners_outward_growth
 depth=depth+pink_corners_outward_growth
 outer=extrude(Circle(r),amount=height)
 top=[e for e in outer.edges() if e.geom_type==GeomType.CIRCLE and abs(e.center().Z-height)<0.001]
 outer=fillet(top,radius=top_radius)
 lower=[e for e in outer.edges() if e.geom_type==GeomType.CIRCLE and abs(e.center().Z)<0.001]
 outer=fillet(lower,radius=corner_edge_radius)
 inner=Pos(0,0,-1)*extrude(Circle(r-depth),amount=height+2)
 quarter=(outer-inner) & (Pos(r/2,r/2,height/2)*Box(r,r,height))
 seams=list(quarter.edges().filter_by(Axis.Z))
 quarter=fillet(seams,radius=corner_guard_seam_radius)
 assert quarter.is_valid and len(quarter.solids())==1
 return quarter
lower=guard(corner_lower_fit_radius,corner_guard_depth,corner_lower_height,corner_edge_radius)
upper=guard(upper_radius,corner_guard_depth,corner_upper_height,corner_guard_upper_top_radius)
caps=[]
for rotation in (0,90,180,270):
 caps.append(Rot(0,0,rotation)*Pos(corner_lower_fit_width/2-corner_lower_fit_radius,corner_lower_fit_width/2-corner_lower_fit_radius,0)*lower)
 caps.append(Rot(0,0,rotation)*Pos(upper_width/2-upper_radius,upper_width/2-upper_radius,corner_upper_z)*upper)
pink=Compound(children=caps)
assert len(pink.solids())==8
pink.color=Color(1.0,0.52,0.69)
publish("pink_corners",pink,"Rounded pink corner guards",material="pla")
