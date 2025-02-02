resource "azurerm_resource_group" "rg" {
  name     = "${var.prefix}-resources"
  location = "southindia"
}