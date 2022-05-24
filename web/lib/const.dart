import 'dart:html' as html;

import 'package:collapsible_sidebar/collapsible_sidebar.dart';
import 'package:flutter/material.dart';
import 'package:swatch/routes/route_color_playground.dart';
import 'package:swatch/routes/route_dashboard.dart';

/// Widgets

List<CollapsibleItem> getSidebarRoutes(BuildContext context) {
  return [
    CollapsibleItem(
      text: "Dashboard",
      icon: Icons.dashboard_outlined,
      onPressed: () =>
          Navigator.of(context).pushReplacementNamed(DashboardRoute.route),
    ),
    CollapsibleItem(
      text: "Color Playground",
      icon: Icons.colorize_outlined,
      onPressed: () => Navigator.of(context)
          .pushReplacementNamed(ColorPlaygroundRoute.route),
    ),
    CollapsibleItem(
      text: "Settings",
      icon: Icons.settings_outlined,
      isSelected: true,
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