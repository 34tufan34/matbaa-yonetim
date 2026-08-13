enum SyncState { pending, syncing, synced, conflict, failed }

class PendingMutation {
  const PendingMutation({
    required this.clientMutationId,
    required this.deviceId,
    required this.entityType,
    required this.entityId,
    required this.operation,
    required this.baseVersion,
    required this.occurredAt,
    required this.payload,
    this.state = SyncState.pending,
  });

  final String clientMutationId;
  final String deviceId;
  final String entityType;
  final String entityId;
  final String operation;
  final int baseVersion;
  final DateTime occurredAt;
  final Map<String, Object?> payload;
  final SyncState state;
}
