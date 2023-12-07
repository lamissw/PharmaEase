import 'dart:async';
import 'package:pharmaease/src/ui/screens/HomePage/map.dart';
import 'package:flutter/material.dart';
import 'package:pharmaease/src/ui/screens/pharmacy_details_screen.dart';
import 'package:pharmaease/src/ui/theme/colors.dart';
import 'package:pharmaease/src/ui/widgets/search_bar_widget.dart';
import 'package:pharmaease/src/ui/widgets/side_menu.dart';

class MapPage extends StatefulWidget {
  const MapPage({super.key});

  @override
  State<MapPage> createState() => _MapPageState();
}

class _MapPageState extends State<MapPage> {
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();

  // List<Map<String, String>> pharmacyList = [
  //   {"title": "Pharmacy 1", "trailing": "6 mins"},
  //   {"title": "Pharmacy 2", "trailing": "4 mins"},
  //   {"title": "Pharmacy 3", "trailing": "8 mins"},
  //   {"title": "Pharmacy 4", "trailing": "8 mins"},
  // ];

  @override
  void initState() {
    super.initState();

    Timer(const Duration(seconds: 0), () {
      _scaffoldKey.currentState!.showBottomSheet(
        (context) => ClipRRect(
          borderRadius: const BorderRadius.vertical(top: Radius.circular(15)),
          child: Container(
            child: buildBottomSheetContent(context),
          ),
        ),
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: _scaffoldKey,
      appBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.menu),
          color: Colors.black,
          onPressed: () {
            _scaffoldKey.currentState!.openDrawer();
          },
        ),
        title: const Row(
          children: [
            Text(
              'PharmaEase',
              style: TextStyle(color: Colors.black),
            ),
          ],
        ),
        backgroundColor: Colors.white,
      ),
      drawer: const Drawer(
        child: SideMenu(),
      ),
      body: Center(
        child: Stack(
          children: <Widget>[
            const Map(),
            Positioned(
              bottom: 0,
              left: 0,
              right: 0,
              child: Container(
                color: Colors.transparent,
                child: buildBottomSheetContent(context),
              ),
            ),
            const searchBar(),
          ],
        ),
      ),
    );
  }

  Widget buildBottomSheetContent(BuildContext context) {
    return SizedBox(
      height: MediaQuery.of(context).size.height*0.25,
      child: Column(
        children: <Widget>[
          const SizedBox(
            height: 15,
          ),
          const Padding(
            padding: EdgeInsets.all(8.0),
            child: Row(
              children: [
                Text(
                  "Nearest Pharmacies",
                  style: TextStyle(fontWeight: FontWeight.w500),
                ),
                // SizedBox(
                //   width: 100,
                // ),
                const Spacer(),
                Padding(
                  padding: EdgeInsets.symmetric(horizontal: 10.0),
                  child: Text("View all Pharmacies"),
                ),
              ],
            ),
          ),
          const SizedBox(
            height: 20,
          ),
          Expanded(
            child: ListView.builder(
              itemCount: 5,
              // pharmacyList.length,
              itemBuilder: (context, index) {
                return Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Container(
                    decoration: const BoxDecoration(
                      shape: BoxShape.rectangle,
                      borderRadius: BorderRadius.all(Radius.circular(15)),
                      color: pharmaGreenColor,
                    ),
                    child: ListTile(
                      title: const Text("title"),
                      trailing: const Text("trailing"),
                      leading: const Icon(Icons.pin_drop),
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                              builder: (context) =>
                                  const PharmacyDetailsScreen()),
                          // title: Text(pharmacyList[index]["title"] ?? ""),
                          // trailing: Text(pharmacyList[index]["trailing"] ?? ""),
                          // leading: Icon(Icons.pin_drop),
                        );
                      },
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
