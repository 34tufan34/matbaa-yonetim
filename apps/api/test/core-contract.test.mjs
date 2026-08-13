import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

const schemaUrl = new URL('../prisma/schema.prisma', import.meta.url);
const permissionUrl = new URL('../src/common/rbac/permission.ts', import.meta.url);

test('Faz 1 veri omurgası kritik tabloları içerir', async () => {
  const schema = await readFile(schemaUrl, 'utf8');

  for (const model of [
    'Organization',
    'User',
    'Role',
    'Permission',
    'SystemDictionary',
    'AppSetting',
    'AuditLog',
  ]) {
    assert.match(schema, new RegExp(`model ${model}\\s*\\{`));
  }
});

test('Kritik işlem izinleri merkezi sözlükte tanımlıdır', async () => {
  const permissionSource = await readFile(permissionUrl, 'utf8');

  for (const code of [
    'production.start',
    'quality.approve',
    'shipment.approve',
    'audit.read',
  ]) {
    assert.ok(permissionSource.includes(code), `${code} izni bulunamadı`);
  }
});
