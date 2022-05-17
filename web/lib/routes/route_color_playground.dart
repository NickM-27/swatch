import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:swatch/api/api.dart';

import 'package:collapsible_sidebar/collapsible_sidebar.dart';
import 'package:swatch/routes/route_dashboard.dart';
import 'package:swatch/routes/route_settings.dart';
import 'package:swatch/theme/theme_helper.dart';

class ColorPlaygroundRoute extends StatefulWidget {
  static const String route = '/color_playground';

  const ColorPlaygroundRoute({Key? key}) : super(key: key);

  @override
  ColorPlaygroundRouteState createState() => ColorPlaygroundRouteState();
}

class ColorPlaygroundRouteState extends State<ColorPlaygroundRoute> {
  late List<CollapsibleItem> _routes;

  @override
  void initState() {
    super.initState();
    _routes = _generateRoutes;
  }

  List<CollapsibleItem> get _generateRoutes {
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
        isSelected: true,
        onPressed: () {},
      ),
      CollapsibleItem(
        text: "Settings",
        icon: Icons.settings_outlined,
        onPressed: () =>
            Navigator.of(context).pushReplacementNamed(SettingsRoute.route),
      ),
    ];
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Swatch"),
        centerTitle: false,
        backgroundColor: SwatchColors.getPrimaryColor(),
      ),
      body: SafeArea(
        child: Stack(
          children: [
            Align(
              alignment: Alignment.centerLeft,
              child: CollapsibleSidebar(
                isCollapsed: true,
                items: _routes,
                avatarImg: const NetworkImage(
                  "https://raw.githubusercontent.com/NickM-27/swatch/master/assets/swatch.png",
                ),
                body: _ColorPlaygroundView(),
                backgroundColor: Colors.blueGrey[700]!,
                selectedTextColor: SwatchColors.getPrimaryColor(),
                iconSize: 24,
                borderRadius: 12,
                sidebarBoxShadow: const [],
                title: "Swatch",
                textStyle: const TextStyle(
                  fontSize: 16,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _ColorPlaygroundView extends StatefulWidget {
  @override
  _ColorPlaygroundViewState createState() => _ColorPlaygroundViewState();
}

class _ColorPlaygroundViewState extends State<_ColorPlaygroundView> {
  final SwatchApi _api = SwatchApi();

  // Objects for steps
  String _source = "";
  Uint8List _imageBytes = Uint8List(0);

  @override
  Widget build(BuildContext context) {
    if (_source.isEmpty) {
      return _SetPicSource(
          (imageSource) => setState(() => _source = imageSource));
    } else if (_imageBytes.isEmpty) {
      return _SaveOrCropImage(_source, (text) async {
        final bytes = await _api.getImageBytes(_source);
        setState(() => _imageBytes = bytes);
      });
    } else if (_source.isNotEmpty && _imageBytes.isNotEmpty) {
      return _AdjustColorValues(_source);
    }

    return const SizedBox();
  }
}

class _SetPicSource extends StatelessWidget {
  final Function(String) _submit;
  String _source = "";

  _SetPicSource(this._submit, {Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      alignment: Alignment.center,
      child: SizedBox(
        width: 300.0,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Padding(
              padding: EdgeInsets.all(8.0),
              child: Text(
                  "Enter the URL source for this cameras image that will be in the config."),
            ),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: TextField(
                onSubmitted: (text) => _submit(_source),
                onChanged: (text) => _source = text,
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: MaterialButton(
                color: SwatchColors.getPrimaryColor(),
                child: const Text("Set Source"),
                onPressed: () => _submit(_source),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _SaveOrCropImage extends StatelessWidget {
  final Function(String) _submit;
  String _imageSource;

  _SaveOrCropImage(this._imageSource, this._submit, {Key? key})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      alignment: Alignment.center,
      child: SizedBox(
        width: 300.0,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Image.network(
                _imageSource,
              ),
            ),
            const Padding(
              padding: EdgeInsets.all(8.0),
              child: Text(
                  "This is the image that will be used to create color values, it can be cropped if you'd like, otherwise submit."),
            ),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: MaterialButton(
                color: SwatchColors.getPrimaryColor(),
                child: const Text("Submit Image"),
                onPressed: () => _submit(_imageSource),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _AdjustColorValues extends StatefulWidget {
  final String _imageSource;

  const _AdjustColorValues(this._imageSource, {Key? key}) : super(key: key);

  @override
  _AdjustColorValuesState createState() => _AdjustColorValuesState();
}

class _AdjustColorValuesState extends State<_AdjustColorValues> {
  final SwatchApi _api = SwatchApi();
  Uint8List _maskImage = Uint8List(0);

  // Lower Color Values
  double _lowRed = 0;
  double _lowGreen = 0;
  double _lowBlue = 0;

  // Upper Color Values
  double _upRed = 255;
  double _upGreen = 255;
  double _upBlue = 255;

  @override
  Widget build(BuildContext context) {
    return Container(
      alignment: Alignment.center,
      child: Row(
        children: [
          Column(
            children: [
              Card(
                child: Column(children: [
                  const Text("Min Acceptable Color Values"),
                  Slider(value: _lowRed, onChanged: (r) => _lowRed = r),
                  Slider(value: _lowGreen, onChanged: (g) => _lowGreen = g),
                  Slider(value: _lowBlue, onChanged: (b) => _lowBlue = b),
                ],),
              ),
              Card(
                child: Column(
                  children: [
                    const Text("Max Acceptable Color Values"),
                    Slider(value: _upRed, onChanged: (r) => _upRed = r),
                    Slider(value: _upGreen, onChanged: (g) => _upGreen = g),
                    Slider(value: _upBlue, onChanged: (b) => _upBlue = b),
                  ],
                ),
              )
            ],
          ),
          Column(
            children: [
              Image.network(widget._imageSource),
              Image.memory(_maskImage)
            ],
          ),
        ],
      ),
    );
  }
}
