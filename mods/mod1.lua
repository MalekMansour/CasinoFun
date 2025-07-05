-- mod1.lua
-- Simple Cyberpunk Mod: Adds a neon glow effect to all players at night

local function is_night()
    local hour = os.date("*t").hour
    return hour >= 20 or hour < 6
end

local function apply_neon_glow(player)
    -- Example: Set player color to neon blue and add a glow effect
    player:set_color({r=0, g=200, b=255})
    player:set_glow(true)
end

local function remove_neon_glow(player)
    player:set_color({r=255, g=255, b=255})
    player:set_glow(false)
end

local function update_players()
    for _, player in ipairs(game.get_players()) do
        if is_night() then
            apply_neon_glow(player)
        else
            remove_neon_glow(player)
        end
    end
end

-- Run update every minute
game.on_interval(60, update_players)