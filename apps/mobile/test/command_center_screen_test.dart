import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:matbaa_mobile/features/command_center/presentation/command_center_screen.dart';

void main() {
  testWidgets('Komuta Merkezi temel kartları görünür', (tester) async {
    await tester.pumpWidget(
      const MaterialApp(home: CommandCenterScreen()),
    );

    expect(find.text('Komuta Merkezi'), findsOneWidget);
    expect(find.text('Aktif işler'), findsOneWidget);
    expect(find.text('Makine durumu'), findsOneWidget);
    expect(find.text('Kritik uyarılar'), findsOneWidget);
    expect(find.text('Vardiya hedefi'), findsOneWidget);
  });
}
