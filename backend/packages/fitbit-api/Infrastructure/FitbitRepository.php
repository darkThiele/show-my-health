<?php

namespace Packages\FitbitApi\Infrastructure;

use Illuminate\Support\Facades\Http;
use Packages\FitbitApi\Domain\Token;

class FitbitRepository
{
    public function getFitbitData(Token $token, string $uri)
    {
        $response = Http::withHeaders([
            'accept' => 'application/json',
            'authorization' => 'Bearer' . $token->accessToken
        ])->get($uri);
        return $response->json();
    }
}
