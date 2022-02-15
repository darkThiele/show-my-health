<?php

namespace Packages\FitbitApi\Domain;

use DateTime;

class Token
{
    public string $id;
    public ?string $accessToken;
    public ?string $refreshToken;
    public ?DateTime $expiresIn;

    public static function by(
        string $id,
        ?string $accessToken,
        ?string $refreshToken,
        ?DateTime $expiresIn
    ): Token {
        $instance = new self();
        $instance->id = $id;
        $instance->accessToken = $accessToken;
        $instance->refreshToken = $refreshToken;
        $instance->expiresIn = $expiresIn;
        return $instance;
    }
}
