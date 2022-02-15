<?php

namespace Packages\HeartRate\Infrastructure;

use DateTime;

class FitbitHeartRateRepository
{
    public function fetchHeartRates(DateTime $start, DateTime $end)
    {
        $date = $start->format('yyyy-MM-dd');
        $startTime = $start->format('HH:mm');
        $endTime = $end->format('HH:mm');
    }
}
