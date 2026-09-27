const nodemailer = require('nodemailer');

// Send email notifications when a session is scheduled.
// Configured to use Gmail SMTP when EMAIL_USER & EMAIL_PASS are set in .env,
// or Ethereal Test SMTP auto-fallback for instant email preview links.
const sendEmail = async ({ to, subject, html }) => {
  try {
    let transporter;

    // Check if real Gmail credentials are set in .env
    const isRealGmail = process.env.EMAIL_USER &&
                        process.env.EMAIL_USER !== 'demo@gyaansetu.com' &&
                        process.env.EMAIL_PASS &&
                        process.env.EMAIL_PASS !== 'demopassword';

    if (isRealGmail) {
      transporter = nodemailer.createTransport({
        service: 'gmail',
        auth: {
          user: process.env.EMAIL_USER,
          pass: process.env.EMAIL_PASS.replace(/\s+/g, '')
        }
      });

      try {
        const mailOptions = {
          from: `"GyaanSetu Platform" <${process.env.EMAIL_USER}>`,
          to,
          subject,
          html
        };
        const info = await transporter.sendMail(mailOptions);
        console.log(`✉️ Gmail notification sent successfully to ${to} (Message ID: ${info.messageId})`);
        return true;
      } catch (gmailErr) {
        console.warn(`⚠️ [Gmail SMTP Warning] ${gmailErr.message}`);
        console.warn(`👉 To fix Gmail SMTP: Ensure 2-Step Verification is ON for ${process.env.EMAIL_USER} and generate a 16-character App Password at https://myaccount.google.com/apppasswords`);
        console.warn(`🔄 Falling back to Ethereal Test SMTP for email preview link...`);
      }
    }

    // Auto-fallback: Generate temporary Ethereal test account for instant testing
    const testAccount = await nodemailer.createTestAccount();
    transporter = nodemailer.createTransport({
      host: 'smtp.ethereal.email',
      port: 587,
      secure: false,
      auth: {
        user: testAccount.user,
        pass: testAccount.pass
      }
    });

    const mailOptions = {
      from: `"GyaanSetu Platform" <no-reply@gyaansetu.com>`,
      to,
      subject,
      html
    };

    const info = await transporter.sendMail(mailOptions);
    console.log(`✉️ Test Email notification sent to ${to} (Message ID: ${info.messageId})`);

    const previewUrl = nodemailer.getTestMessageUrl(info);
    if (previewUrl) {
      console.log(`🔗 Preview Email Online Link: ${previewUrl}`);
    }

    return true;
  } catch (error) {
    console.warn(`[Nodemailer Notice] Could not send email to ${to}: ${error.message}`);
    return false;
  }
};

module.exports = sendEmail;
