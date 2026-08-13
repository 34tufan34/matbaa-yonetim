import { Injectable } from '@nestjs/common';
import { Prisma } from '../../generated/prisma/client';
import { PrismaService } from '../../prisma/prisma.service';

export type AuditWrite = {
  organizationId: string;
  actorUserId?: string;
  entityType: string;
  entityId: string;
  action: 'CREATE' | 'UPDATE' | 'DELETE' | 'APPROVE' | 'REJECT' | 'LOGIN' | 'SYNC';
  oldValue?: unknown;
  newValue?: unknown;
  reason?: string;
  deviceId?: string;
  correlationId?: string;
};

@Injectable()
export class AuditService {
  constructor(private readonly prisma: PrismaService) {}

  write(entry: AuditWrite) {
    return this.prisma.auditLog.create({
      data: {
        organizationId: entry.organizationId,
        actorUserId: entry.actorUserId,
        entityType: entry.entityType,
        entityId: entry.entityId,
        action: entry.action,
        oldValue: entry.oldValue as Prisma.InputJsonValue | undefined,
        newValue: entry.newValue as Prisma.InputJsonValue | undefined,
        reason: entry.reason,
        deviceId: entry.deviceId,
        correlationId: entry.correlationId,
      },
    });
  }
}
