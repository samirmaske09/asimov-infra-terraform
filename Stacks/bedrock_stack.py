from constructs import Construct
from providers import AwsBaseStack

# Resource class names can vary by provider version. Examples below use typical names:
from cdktf_cdktf_provider_aws.bedrockagent_agent import BedrockagentAgent
from cdktf_cdktf_provider_aws.bedrockagent_agent_action_group import BedrockagentAgentActionGroup
from cdktf_cdktf_provider_aws.bedrock_guardrail import BedrockGuardrail
from cdktf_cdktf_provider_aws.bedrock_knowledge_base import BedrockKnowledgeBase

class AIBedrockStack(AwsBaseStack):
    def __init__(self, scope: Construct, id: str, ctx, data_bucket_name: str, kms_key_id: str):
        super().__init__(scope, id, ctx)

        # Guardrail
        self.guardrail = BedrockGuardrail(self, "gr",
            name=f"{ctx.name_prefix}-guardrail",
            blocked_input_categories=["HATE", "VIOLENCE"],
            blocked_output_categories=["HATE", "VIOLENCE"]
        )

        # Knowledge Base (example: S3 data source)
        self.kb = BedrockKnowledgeBase(self, "kb",
            name=f"{ctx.name_prefix}-kb",
            description="Docs KB",
            storage_configuration={
              "type": "S3",
              "s3Configuration": {"bucketName": data_bucket_name, "inclusionPrefixes": ["kb/"]}
            },
            encryption_configuration={"kmsKeyId": kms_key_id}
        )

        # Agent
        self.agent = BedrockagentAgent(self, "agent",
            name=f"{ctx.name_prefix}-agent",
            description="Customer support agent",
            instruction="You are a helpful assistant.",
            guardrail_configuration={"guardrailIdentifier": self.guardrail.id},
            knowledge_bases=[{"knowledgeBaseId": self.kb.id}]
        )

        # Action Group
        self.ag = BedrockagentAgentActionGroup(self, "ag",
            agent_id=self.agent.id,
            name="searchDocs",
            action_group_state="ENABLED",
            api_schema={"payload": "openapi spec or function schema JSON here"}
        )
