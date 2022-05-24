import 'dart:html' as html;

import 'package:collapsible_sidebar/collapsible_sidebar.dart';
import 'package:flutter/material.dart';
import 'package:swatch/routes/route_color_playground.dart';
import 'package:swatch/routes/route_dashboard.dart';
import 'package:swatch/routes/route_detections.dart';
import 'package:swatch/routes/route_settings.dart';

/// Widgets

List<CollapsibleItem> getSidebarRoutes(
  BuildContext context,
  String name,
) {
  return [
    CollapsibleItem(
      text: "Dashboard",
      icon: Icons.dashboard_outlined,
      isSelected: name == DashboardRoute.route,
      onPressed: () =>
          Navigator.of(context).pushReplacementNamed(DashboardRoute.route),
    ),
    CollapsibleItem(
      text: "Detections",
      icon: Icons.event_note_outlined,
      isSelected: name == DetectionListRoute.route,
      onPressed: () =>
          Navigator.of(context).pushReplacementNamed(DetectionListRoute.route),
    ),
    CollapsibleItem(
      text: "Color Playground",
      icon: Icons.colorize_outlined,
      isSelected: name == ColorPlaygroundRoute.route,
      onPressed: () => Navigator.of(context)
          .pushReplacementNamed(ColorPlaygroundRoute.route),
    ),
    CollapsibleItem(
      text: "Settings",
      icon: Icons.settings_outlined,
      isSelected: name == SettingsRoute.route,
      onPressed: () {},
    ),
    CollapsibleItem(
      text: "GitHub",
      icon: Icons.code,
      isSelected: false,
      onPressed: () => html.window.open(urlGitHubReadme, "swatch-readme"),
    ),
    CollapsibleItem(
      text: "Docs",
      icon: Icons.mark_chat_read_outlined,
      isSelected: false,
      onPressed: () => html.window.open(urlGitHubDocs, "swatch-docs"),
    ),
  ];
}

/// URLs
const urlGitHubReadme = "https://github.com/NickM-27/swatch";
const urlGitHubDocs = "https://github.com/NickM-27/swatch/tree/main/docs";
