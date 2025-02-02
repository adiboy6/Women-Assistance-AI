variable "prefix" {
  default = "hackviolet"
}

variable "openai_deployments" {
  description = "(Optional) Specifies the deployments of the Azure OpenAI Service"
  type = list(object({
    name = string
    model = object({
      name = string
    })
    rai_policy_name = string  
  }))
  default = [
    {
      name = "gpt-4"
      model = {
        name = "gpt-4"
        # version = "0301"
      }
      rai_policy_name = ""
    }
  ] 
}