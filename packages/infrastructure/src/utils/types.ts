import { z } from 'zod'

export const DeploymentEnvironmentSchema = z.enum(['development', 'production'])

export type DeploymentEnvironment = z.infer<typeof DeploymentEnvironmentSchema>
