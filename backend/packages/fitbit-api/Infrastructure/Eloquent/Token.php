<?php

namespace Packages\FitbitApi\Infrastructure;

use DateTime;
use Illuminate\Database\Eloquent\Model;

/**
 * @property string $id
 * @property string $accessToken
 * @property string $refreshToken
 * @property DateTime $expiresIn
 */
class Token extends Model
{
    public function toDomainModel(): \Packages\FitbitApi\Domain\Token
    {
        return \Packages\FitbitApi\Domain\Token::by(
            $this->id,
            $this->accessToken,
            $this->refreshToken,
            $this->expiresIn
        );
    }
}
