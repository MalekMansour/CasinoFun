-- Cyberpunk Mod: Give $1 to player every time 'W' is pressed

local playerMoney = 0

-- Function to add money
local function giveMoney(amount)
    playerMoney = playerMoney + amount
    print("You received $1! Total money: $" .. playerMoney)
end

-- Key press handler
function love.keypressed(key)
    if key == "w" then
        giveMoney(1)
    end
end

-- Optional: Draw money on screen (if using LÖVE framework)
function love.draw()
    love.graphics.print("Money: $" .. playerMoney, 10, 10)
end