import 'dart:async';
import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Divvy',
      theme: ThemeData(
          brightness: Brightness.dark,
          primaryColor: Colors.black,
          primarySwatch: Colors.blue,
          backgroundColor: Colors.black),
      home: MyHomePage(title: 'Divvy'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  final String title;
  MyHomePage({Key key, this.title}) : super(key: key);

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

Future<void> _payWithVenmo() async {
  double balance = 130.95;
  String url =
      'venmo://paycharge?txn=pay&recipients=ArjunMitra&amount=$balance&note=Divvy';
  if (await canLaunch(url)) {
    await launch(url);
  } else {
    throw 'Could not launch $url';
  }
}

AspectRatio balanceDisplay = AspectRatio(
    aspectRatio: 2,
    child: Container(
        // color: Theme.of(context).primaryColor,
        color: Colors.black,
        child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Text('Balance', style: TextStyle(fontSize: 30)),
              Text('\$130.95', style: TextStyle(fontSize: 80)),
            ])));

Container sendButton = Container(
    width: 80,
    height: 80,
    child: FloatingActionButton(
      onPressed: () => _payWithVenmo(),
      child: Icon(
        Icons.attach_money,
        size: 50,
      ),
    ));

class _MyHomePageState extends State<MyHomePage> {
  @override
  Widget build(BuildContext context) {
    double balance = 130.95;
    return Scaffold(
      backgroundColor: Theme.of(context).backgroundColor,
      appBar: AppBar(
        title: Text(widget.title),
      ),
      floatingActionButton: sendButton,
      body: ListView(
        children: <Widget>[
          Divider(color: Colors.white),
          Column(
            children: <Widget>[balanceDisplay],
          ),
        ],
      ),
    );
  }
}
