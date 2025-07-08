-- Simple terminal version: Give $1 to player every time 'w' is entered

local playerMoney = 0

while true do
    io.write("Press 'w' and Enter to get $1 (or 'q' to quit): ")
    local input = io.read()
    if input == "w" then
        playerMoney = playerMoney + 1
        print("You received $1! Total money: $" .. playerMoney)
    elseif input == "q" then
        print("Goodbye! Final money: $" .. playerMoney)
        break
    else
        print("Invalid input.")
    end
end
