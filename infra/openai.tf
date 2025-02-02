####==========Create openAI resource ======#####
resource "azurerm_cognitive_account" "openai" {
  name                          = "women-assistance-agent"
  location                      = azurerm_resource_group.rg.location
  resource_group_name           = azurerm_resource_group.rg.name
  kind                          = "OpenAI"
  sku_name                      = "S0"
  public_network_access_enabled = true
  tags = {
    Acceptance = "Test"
    Prefix = var.prefix
  }

  identity {
    type = "SystemAssigned"
  }

  lifecycle {
    ignore_changes = [
      tags
    ]
  }
}

# resource "azurerm_cognitive_deployment" "deployment" {
#   for_each             = {for deployment in var.openai_deployments: deployment.name => deployment}

#   name                 = each.key
#   cognitive_account_id = azurerm_cognitive_account.openai.id

#   model {
#     format  = "OpenAI"
#     name    = each.value.model.name
#   }

#   sku {
#     name = "Standard"
#   }
# }