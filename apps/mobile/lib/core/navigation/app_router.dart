import 'package:go_router/go_router.dart';
import '../../features/command_center/presentation/command_center_screen.dart';

final appRouter = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const CommandCenterScreen(),
    ),
  ],
);
