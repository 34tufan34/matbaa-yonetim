import 'package:flutter/material.dart';

class CommandCenterScreen extends StatelessWidget {
  const CommandCenterScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.sizeOf(context).width;
    final columns = width >= 1100 ? 4 : width >= 700 ? 2 : 1;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Komuta Merkezi'),
        actions: const [
          Padding(
            padding: EdgeInsets.symmetric(horizontal: 16),
            child: Center(child: Text('Çevrimdışı hazır')),
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Fabrika durumu', style: Theme.of(context).textTheme.headlineSmall),
            const SizedBox(height: 12),
            Expanded(
              child: GridView.count(
                crossAxisCount: columns,
                crossAxisSpacing: 12,
                mainAxisSpacing: 12,
                childAspectRatio: width >= 700 ? 1.9 : 2.5,
                children: const [
                  _StatusCard(title: 'Aktif işler', value: '—', subtitle: 'Canlı veri bağlanacak'),
                  _StatusCard(title: 'Makine durumu', value: '—', subtitle: 'Çalışıyor / duruş / arıza'),
                  _StatusCard(title: 'Kritik uyarılar', value: '—', subtitle: 'Önceliklendirilmiş olaylar'),
                  _StatusCard(title: 'Vardiya hedefi', value: '—', subtitle: 'Hedef / gerçekleşen'),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _StatusCard extends StatelessWidget {
  const _StatusCard({required this.title, required this.value, required this.subtitle});
  final String title;
  final String value;
  final String subtitle;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(title, style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 8),
            Text(value, style: Theme.of(context).textTheme.headlineMedium),
            const SizedBox(height: 4),
            Text(subtitle, maxLines: 2, overflow: TextOverflow.ellipsis),
          ],
        ),
      ),
    );
  }
}
