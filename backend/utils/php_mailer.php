<?php
/**
 * VisionEdge PHP Mailer for Email OTP Verification
 * Supports:
 * 1. Direct SMTP via SSL/TLS socket (Gmail, Outlook, Custom SMTP)
 * 2. PHP native mail() fallback
 * Usage: php php_mailer.php <to_email> <subject> <otp_code> [user_name]
 */

if ($argc < 4) {
    echo json_encode(["success" => false, "message" => "Usage: php php_mailer.php <to_email> <subject> <otp_code> [user_name]"]);
    exit(1);
}

$toEmail   = trim($argv[1]);
$subject   = trim($argv[2]);
$otpCode   = trim($argv[3]);
$userName  = isset($argv[4]) && !empty($argv[4]) ? trim($argv[4]) : 'Valued Customer';

// Load .env variables if present
$envFile = dirname(__DIR__) . '/.env';
$env = [];
if (file_exists($envFile)) {
    $lines = file($envFile, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    foreach ($lines as $line) {
        $line = trim($line);
        if ($line === '' || str_starts_with($line, '#')) continue;
        if (str_contains($line, '=')) {
            list($key, $val) = explode('=', $line, 2);
            $env[trim($key)] = trim($val, " \t\n\r\0\x0B\"'");
        }
    }
}

$smtpHost = getenv('SMTP_HOST') ?: ($env['SMTP_HOST'] ?? 'smtp.gmail.com');
$smtpPort = intval(getenv('SMTP_PORT') ?: ($env['SMTP_PORT'] ?? 587));
$smtpUser = getenv('SMTP_EMAIL') ?: ($env['SMTP_EMAIL'] ?? ($env['SMTP_USER'] ?? 'chaudharidevanshu1912@gmail.com'));
$smtpPass = getenv('SMTP_PASSWORD') ?: ($env['SMTP_PASSWORD'] ?? ($env['SMTP_PASS'] ?? ''));
$fromName = "VisionEdge Eyewear";

$htmlBody = <<<HTML
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>VisionEdge Verification Code</title>
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f8fafc; margin: 0; padding: 24px;">
    <div style="max-width: 520px; margin: 0 auto; background: #ffffff; border-radius: 16px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
        <div style="background: linear-gradient(135deg, #0d6efd, #0b5ed7); padding: 32px 24px; text-align: center; color: #ffffff;">
            <h1 style="margin: 0; font-size: 24px; font-weight: 700; letter-spacing: -0.5px;">VisionEdge</h1>
            <p style="margin: 8px 0 0; opacity: 0.9; font-size: 14px;">Next-Gen Eyewear & Eye Care</p>
        </div>
        <div style="padding: 32px 24px;">
            <p style="font-size: 16px; color: #1e293b; margin-top: 0;">Hello <strong>{$userName}</strong>,</p>
            <p style="font-size: 14px; color: #475569; line-height: 1.6;">Use the verification code below to complete your login to your VisionEdge account. This code is valid for <strong>10 minutes</strong>.</p>
            
            <div style="margin: 28px 0; text-align: center;">
                <div style="display: inline-block; background: #f1f5f9; border: 2px dashed #0d6efd; border-radius: 12px; padding: 14px 32px;">
                    <span style="font-family: monospace; font-size: 32px; font-weight: bold; letter-spacing: 8px; color: #0d6efd;">{$otpCode}</span>
                </div>
            </div>

            <p style="font-size: 13px; color: #64748b; line-height: 1.5; margin-bottom: 24px;">
                If you did not request this login code, you can safely ignore this email. Someone may have typed your email address by mistake.
            </p>

            <div style="border-top: 1px solid #e2e8f0; padding-top: 20px; font-size: 12px; color: #94a3b8; text-align: center;">
                VisionEdge Optical Store &bull; Opp. Sardar Patel Stadium, Navrangpura, Ahmedabad &bull; +91 82382 40028
            </div>
        </div>
    </div>
</body>
</html>
HTML;

function sendViaSmtp($host, $port, $user, $pass, $fromName, $to, $subject, $body) {
    if (empty($pass) || empty($user) || str_starts_with($pass, 'your_')) {
        return ["success" => false, "message" => "SMTP credentials not configured"];
    }

    $timeout = 10;
    $context = stream_context_create([
        'ssl' => [
            'verify_peer' => false,
            'verify_peer_name' => false,
            'allow_self_signed' => true
        ]
    ]);

    $socket = stream_socket_client("tcp://{$host}:{$port}", $errno, $errstr, $timeout, STREAM_CLIENT_CONNECT, $context);
    if (!$socket) {
        return ["success" => false, "message" => "Could not connect to {$host}:{$port}: $errstr ($errno)"];
    }

    $read = function() use ($socket) {
        $response = "";
        while ($line = fgets($socket, 515)) {
            $response .= $line;
            if (substr($line, 3, 1) === ' ') break;
        }
        return $response;
    };

    $send = function($cmd) use ($socket, $read) {
        fputs($socket, $cmd . "\r\n");
        return $read();
    };

    $read(); // Read greeting
    $send("EHLO " . gethostname());
    
    // STARTTLS if port 587
    if ($port == 587) {
        $send("STARTTLS");
        if (!stream_socket_enable_crypto($socket, true, STREAM_CRYPTO_METHOD_TLS_CLIENT)) {
            fclose($socket);
            return ["success" => false, "message" => "Failed to negotiate TLS"];
        }
        $send("EHLO " . gethostname());
    }

    // AUTH LOGIN
    $res = $send("AUTH LOGIN");
    if (!str_starts_with($res, "334")) {
        fclose($socket);
        return ["success" => false, "message" => "AUTH LOGIN rejected: $res"];
    }

    $send(base64_encode($user));
    $res = $send(base64_encode($pass));
    if (!str_starts_with($res, "235")) {
        fclose($socket);
        return ["success" => false, "message" => "SMTP Authentication failed: $res"];
    }

    $send("MAIL FROM:<{$user}>");
    $send("RCPT TO:<{$to}>");
    $send("DATA");

    $headers  = "MIME-Version: 1.0\r\n";
    $headers .= "Content-Type: text/html; charset=UTF-8\r\n";
    $headers .= "From: {$fromName} <{$user}>\r\n";
    $headers .= "To: {$to}\r\n";
    $headers .= "Subject: {$subject}\r\n";
    $headers .= "Date: " . date('r') . "\r\n";

    $res = $send($headers . "\r\n" . $body . "\r\n.");
    $send("QUIT");
    fclose($socket);

    if (str_starts_with($res, "250")) {
        return ["success" => true, "message" => "Email dispatched successfully via SMTP."];
    }
    return ["success" => false, "message" => "Failed to deliver data: $res"];
}

// Attempt SMTP
$result = sendViaSmtp($smtpHost, $smtpPort, $smtpUser, $smtpPass, $fromName, $toEmail, $subject, $htmlBody);

if (!$result['success']) {
    // Attempt PHP native mail() as secondary
    $headers  = "MIME-Version: 1.0\r\n";
    $headers .= "Content-Type: text/html; charset=UTF-8\r\n";
    $headers .= "From: {$fromName} <{$smtpUser}>\r\n";
    
    $mailSent = @mail($toEmail, $subject, $htmlBody, $headers);
    if ($mailSent) {
        $result = ["success" => true, "message" => "Email sent via PHP mail() function."];
    }
}

echo json_encode($result);
