const nodemailer = require('nodemailer');

// Send email notifications when a session is scheduled.
// Uses Nodemailer transport configured with environment variables.
// Includes try/catch to ensure app doesn't crash if email server is unavailable.
const sendEmail = async ({ to, subject, html }) => {
  try {
    const transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASS
      }
    });

    const mailOptions = {
      from: `"GyaanSetu Platform" <${process.env.EMAIL_USER || 'no-reply@gyaansetu.com'}>`,
      to,
      subject,
      html
    };

    const info = await transporter.sendMail(mailOptions);
    console.log(`Email sent to ${to}: ${info.messageId}`);
    return true;
  } catch (error) {
    // Log the error but DO NOT throw exception so session creation succeeds anyway
    console.warn(`[Nodemailer Warning] Could not send email to ${to}: ${error.message}`);
    return false;
  }
};

module.exports = sendEmail;
