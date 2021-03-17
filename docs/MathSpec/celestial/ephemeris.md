+ Talk about XB
+ Include light time correction and abberation computations

## Ephemeris frame conversion

??? "check" Validation
    From this state:
    [Earth J2000] 2022-11-30T06:26:37 TAI   position = [191703.640707, 58555.734553, 17306.278555] km       velocity = [1.187466, 0.685439, 0.291848] km/s
    Started with this state:
    [Moon J2000] 2022-11-30T06:26:37 TAI    position = [-139995.632274, 198959.755804, 112933.152325] km    velocity = [0.674319, -0.143505, -0.099761] km/s
    Converted to this state in Nyx:
    [Earth J2000] 2022-11-30T06:26:37 TAI   position = [191703.640707, 58555.734553, 17306.278555] km       velocity = [1.187466, 0.685439, 0.291848] km/s
    Which was then inputed into GMAT, and used GMAT to convert back to Moon J2000, which led to this:
    In Moon J2000 in GMAT:
                                            position = [-139995.616184, 198959.764185, 112933.153003] km    velocity = [0.674318, -0.143505, -0.099760] km/s
