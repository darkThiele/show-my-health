<?php

namespace Packages\FitbitApi\Domain;

use DateTime;

class Token
{
    public string $accessToken;
    public string $refreshToken;
    public DateTime $expiresIn;
}
