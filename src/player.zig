pub const Player = packed struct(u32) {
    // 1    2    3    4    5    6    7    8
    // 1,   3,   7,  15,  31,  63, 127, 255
    position: u8 = 0,

    speed_top: u4,
    speed_bottom: u4,

    max_speed_top: u4,
    max_speed_bottom: u4,

    fuel_mass: u6,
};
