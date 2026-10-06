# cell: rim
# cell: rim
# cell: rim
# cell: rim
# cell: rim
rim_width=param("rim_width",150.0)
rim_opening=param("rim_opening",124.0)
rim_height=param("rim_height",18.0)
rim_corner_radius=param("rim_corner_radius",18.0)
rim_inner_corner_radius=param("rim_inner_corner_radius",5.0)
rim_lip_radius=param("rim_lip_radius",3.0)
rim_inner_lip_radius=param("rim_inner_lip_radius",1.5)
rim_socket_depth=param("rim_socket_depth",9.0)
rim_outward_growth=param("rim_outward_growth",1.0)
rim_inward_growth=param("rim_inward_growth",1.0)
rim_width=rim_width+2*rim_outward_growth
rim_opening=rim_opening-2*rim_inward_growth
rim_corner_radius=rim_corner_radius+rim_outward_growth
rim_inner_corner_radius=rim_inner_corner_radius-rim_inward_growth
rim_z=180-rim_height
wall=(rim_width-rim_opening)/2
inner=RectangleRounded(rim_opening,rim_opening,rim_inner_corner_radius)
profile=RectangleRounded(rim_width,rim_width,rim_corner_radius)-inner
rim=Pos(0,0,rim_z)*extrude(profile,amount=rim_height)
top_edges=list(rim.edges().group_by(Axis.Z)[-1])
outer_edges=[e for e in top_edges if max(abs(e.bounding_box().min.X),abs(e.bounding_box().max.X),abs(e.bounding_box().min.Y),abs(e.bounding_box().max.Y))>rim_width/2-0.01]
rim=fillet(outer_edges,radius=rim_lip_radius)
inner_edges=[e for e in rim.edges() if abs(e.center().Z-180)<0.001 and max(abs(e.bounding_box().min.X),abs(e.bounding_box().max.X),abs(e.bounding_box().min.Y),abs(e.bounding_box().max.Y))<rim_opening/2+0.01]
rim=fillet(inner_edges,radius=rim_inner_lip_radius)
socket_outer=RectangleRounded(rim_width-wall,rim_width-wall,rim_corner_radius-wall/2)
socket=Pos(0,0,rim_z)*extrude(socket_outer-inner,amount=rim_socket_depth)
rim=rim-socket
rim_contact_radius=param("rim_contact_radius",1.0)
contact_edges=[e for e in rim.edges() if abs(e.center().Z-rim_z)<0.001 or abs(e.center().Z-(rim_z+rim_socket_depth))<0.001]
rim=fillet(contact_edges,radius=rim_contact_radius)
rim.color=Color(1.0,0.53,0.70)
publish("pink_rim",rim,"Rounded pink top rim",material="pla")
