const BASE_URL = "http://127.0.0.1:8000";

export async function getSlides() {
  const res = await fetch(`${BASE_URL}/api/slides/`);
  return res.json();
}

export async function getTestimonials() {
  const res = await fetch(`${BASE_URL}/api/testimonials/`);
  return res.json();
}

export async function getSettings() {
  const res = await fetch(`${BASE_URL}/api/settings/`);
  return res.json();
}

export async function getEvents() {
  const res = await fetch(`${BASE_URL}/api/events/`);
  return res.json();
}