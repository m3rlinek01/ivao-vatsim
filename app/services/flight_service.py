import folium
from app.utils.helpers import parse_route, get_waypoint_coordinates

def create_flight_markers(pilots):
    markers = []
    for pilot in pilots:
        try:
            lat, lon = float(pilot[4]), float(pilot[5])
            network = pilot[12]
            callsign = pilot[0]
            aircraft = pilot[1]
            route = pilot[11]

            waypoints = parse_route(route)
            route_coordinates = []
            for wp in waypoints:
                coords = get_waypoint_coordinates(wp)
                if coords:
                    route_coordinates.append(coords)

            table_html = f"""
            <table style="width:100%; border-collapse: collapse; font-family: Arial, sans-serif;">
                <tr><th colspan="2" style="background-color: #f2f2f2; padding: 10px;">{callsign} - {aircraft}</th></tr>
                <tr><td style="padding: 5px;">From</td><td style="padding: 5px;">{pilot[2]}</td></tr>
                <tr><td style="padding: 5px;">To</td><td style="padding: 5px;">{pilot[3]}</td></tr>
                <tr><td style="padding: 5px;">Altitude</td><td style="padding: 5px;">{pilot[6]} ft</td></tr>
                <tr><td style="padding: 5px;">Speed</td><td style="padding: 5px;">{pilot[7]} kts</td></tr>
                <tr><td style="padding: 5px;">Heading</td><td style="padding: 5px;">{pilot[8]}°</td></tr>
                <tr><td style="padding: 5px;">Network</td><td style="padding: 5px;">{network}</td></tr>
                <tr><td style="padding: 5px;">Route</td><td style="padding: 5px; max-width: 200px; overflow-x: auto;">{route}</td></tr>
            </table>
            """

            icon_color = "red" if network == "VATSIM" else "green"

            icon_html = f'''
                <div>
                    <div style="font-size: 24px; color: {icon_color};">✈</div>
                    <div style="font-size: 10pt; color: black; text-align: center; margin-top: -5px;">
                        {callsign}<br>{aircraft}
                    </div>
                </div>
            '''

            icon = folium.DivIcon(html=icon_html)

            marker = folium.Marker(
                [lat, lon],
                icon=icon,
                tooltip=folium.Tooltip(table_html)
            )

            marker.add_child(folium.Element(f"""
                <script>
                    var route_coordinates = {route_coordinates};
                    var route_polyline;
                    $(document).on('click', "div:contains('✈')", function() {{
                        if (typeof route_polyline !== 'undefined') {{
                            map.removeLayer(route_polyline);
                        }}
                        route_polyline = L.polyline(route_coordinates, {{color: '{icon_color}', weight: 2, opacity: 0.8}}).addTo(map);
                    }});
                </script>
            """))

            markers.append(marker)
        except ValueError:
            continue

    return markers