module.exports = { 
    port: process.env.PORT || '5000',
    model_url: process.env.MODEL_URL || 'machine-learning/checkpoints/sfBoot.ckpt',
    runner: process.env.RUNNER || 'machine-learning/main.py'
}