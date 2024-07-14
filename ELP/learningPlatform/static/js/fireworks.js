class Firework {
    constructor(sx, sy, tx, ty) {
        this.pos = { x: sx, y: sy };
        this.target = { x: tx, y: ty };
        this.distanceToTarget = this.calculateDistance(sx, sy, tx, ty);
        this.distanceTraveled = 0;
        this.coordinates = [];
        this.coordinateCount = 3;
        while (this.coordinateCount--) {
            this.coordinates.push([this.pos.x, this.pos.y]);
        }
        this.angle = Math.atan2(ty - sy, tx - sx);
        this.speed = 2;
        this.acceleration = 1.05;
        this.brightness = Math.random() * 50 + 50;
        this.targetRadius = 1;
    }

    update(index) {
        this.coordinates.pop();
        this.coordinates.unshift([this.pos.x, this.pos.y]);
        if (this.targetRadius < 8) {
            this.targetRadius += 0.3;
        } else {
            this.targetRadius = 1;
        }
        this.speed *= this.acceleration;
        const vx = Math.cos(this.angle) * this.speed;
        const vy = Math.sin(this.angle) * this.speed;
        this.distanceTraveled = this.calculateDistance(
            this.pos.x,
            this.pos.y,
            this.pos.x + vx,
            this.pos.y + vy
        );

        if (this.distanceTraveled >= this.distanceToTarget) {
            createParticles(this.target.x, this.target.y);
            fireworks.splice(index, 1);
        } else {
            this.pos.x += vx;
            this.pos.y += vy;
        }
    }

    draw() {
        ctx.beginPath();
        ctx.moveTo(
            this.coordinates[this.coordinates.length - 1][0],
            this.coordinates[this.coordinates.length - 1][1]
        );
        ctx.lineTo(this.pos.x, this.pos.y);
        ctx.strokeStyle = `hsl(${hue}, 100%, ${this.brightness}%)`;
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(this.target.x, this.target.y, this.targetRadius, 0, Math.PI * 2);
        ctx.stroke();
    }

    calculateDistance(sx, sy, tx, ty) {
        const xDistance = tx - sx;
        const yDistance = ty - sy;
        return Math.sqrt(xDistance * xDistance + yDistance * yDistance);
    }
}

class Particle {
    constructor(x, y) {
        this.pos = { x, y };
        this.coordinates = [];
        this.coordinateCount = 5;
        while (this.coordinateCount--) {
            this.coordinates.push([this.pos.x, this.pos.y]);
        }
        this.angle = Math.random() * Math.PI * 2;
        this.speed = Math.random() * 10 + 1;
        this.friction = 0.95;
        this.gravity = 1;
        this.hue = Math.random() * 30 + hue;
        this.brightness = Math.random() * 50 + 50;
        this.alpha = 1;
        this.decay = Math.random() * 0.015 + 0.015;
    }

    update(index) {
        this.coordinates.pop();
        this.coordinates.unshift([this.pos.x, this.pos.y]);
        this.speed *= this.friction;
        this.pos.x += Math.cos(this.angle) * this.speed;
        this.pos.y += Math.sin(this.angle) * this.speed + this.gravity;
        this.alpha -= this.decay;

        if (this.alpha <= this.decay) {
            particles.splice(index, 1);
        }
    }

    draw() {
        ctx.beginPath();
        ctx.moveTo(
            this.coordinates[this.coordinates.length - 1][0],
            this.coordinates[this.coordinates.length - 1][1]
        );
        ctx.lineTo(this.pos.x, this.pos.y);
        ctx.strokeStyle = `hsla(${this.hue}, 100%, ${this.brightness}%, ${this.alpha})`;
        ctx.stroke();
    }
}

const canvas = document.getElementById('fireworks-container');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const fireworks = [];
const particles = [];
let hue = 120;
let limiterTotal = 5;
let limiterTick = 0;
let timerTotal = 80;
let timerTick = 0;
let mousedown = false;
let mx;
let my;

function random(min, max) {
    return Math.random() * (max - min) + min;
}

function createParticles(x, y) {
    let particleCount = 30;
    while (particleCount--) {
        particles.push(new Particle(x, y));
    }
}

function loop() {
    requestAnimationFrame(loop);
    hue += 0.5;
    ctx.globalCompositeOperation = 'destination-out';
    ctx.fillStyle = `rgba(0, 0, 0, 0.5)`;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.globalCompositeOperation = 'lighter';
    let i = fireworks.length;
    while (i--) {
        fireworks[i].draw();
        fireworks[i].update(i);
    }
    let j = particles.length;
    while (j--) {
        particles[j].draw();
        particles[j].update(j);
    }

    if (limiterTick >= limiterTotal) {
        if (mousedown) {
            fireworks.push(new Firework(canvas.width / 2, canvas.height, mx, my));
            limiterTick = 0;
        }
    } else {
        limiterTick++;
    }

    if (timerTick >= timerTotal) {
        if (!mousedown) {
            fireworks.push(
                new Firework(
                    canvas.width / 2,
                    canvas.height,
                    random(0, canvas.width),
                    random(0, canvas.height / 2)
                )
            );
            timerTick = 0;
        }
    } else {
        timerTick++;
    }
}

canvas.addEventListener('mousedown', (e) => {
    e.preventDefault();
    mousedown = true;
    mx = e.pageX - canvas.offsetLeft;
    my = e.pageY - canvas.offsetTop;
});

canvas.addEventListener('mouseup', (e) => {
    e.preventDefault();
    mousedown = false;
});

window.onload = loop;
