import { Injectable } from '@nestjs/common';
import { PrismaService } from '../../prisma/prisma.service';

@Injectable()
export class SystemSettingsService {
  constructor(private readonly prisma: PrismaService) {}

  list(organizationId: string) {
    return this.prisma.appSetting.findMany({
      where: { organizationId },
      orderBy: { key: 'asc' },
    });
  }

  listDictionaries(organizationId: string) {
    return this.prisma.systemDictionary.findMany({
      where: { organizationId },
      include: {
        items: {
          where: { isActive: true },
          orderBy: [{ sortOrder: 'asc' }, { label: 'asc' }],
        },
      },
      orderBy: { name: 'asc' },
    });
  }
}
