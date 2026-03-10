import * as cdk from 'aws-cdk-lib'
import { Template } from 'aws-cdk-lib/assertions'
import { StorageStack } from 'lib/storage.stack'
import { DeploymentEnvironment } from 'utils/types'

export function createStorageTemplate(
  environment: DeploymentEnvironment = 'development'
): Template {
  const app = new cdk.App()
  const stack = new StorageStack(app, 'TestStorage', {
    deploymentEnvironment: environment,
    env: { account: '123456789012', region: 'us-east-1' }
  })
  return Template.fromStack(stack)
}
