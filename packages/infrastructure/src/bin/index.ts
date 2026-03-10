import * as cdk from 'aws-cdk-lib'
import { StorageStack } from 'lib/storage.stack'
import { z } from 'zod'

const envSchema = z.object({
  ENVIRONMENT: z.enum(['development', 'production']),
  AWS_ACCOUNT: z.string(),
  AWS_DEFAULT_REGION: z.string().default('us-east-1')
})

const env = envSchema.parse(process.env)

const cdkEnv = {
  account: env.AWS_ACCOUNT,
  region: env.AWS_DEFAULT_REGION
}

const app = new cdk.App()

new StorageStack(app, 'SymmetriesStorage', {
  deploymentEnvironment: env.ENVIRONMENT,
  env: cdkEnv
})
