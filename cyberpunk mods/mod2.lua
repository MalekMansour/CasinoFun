-- CET version: Adds $1 to player when button is pressed in overlay

local playerMoney = 0

registerForEvent("onDraw", function()
    ImGui.Begin("Money Giver")
    if ImGui.Button("Give $1") then
        playerMoney = playerMoney + 1
        print("You received $1! Total money: $" .. playerMoney)
    end
    ImGui.Text("Total money: $" .. playerMoney)
    ImGui.End()
end)
