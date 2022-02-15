<?php

namespace Packages\HeartRate\Domain;

use DateTime;

class HeartRate
{
    /**
     * @var DateTime 測定時間
     */
    public DateTime $dateTime;

    /**
     * @var int 心拍数
     */
    public int $heartRate;
}
