/* script.js - COMPLETE FILE */

// --- PART 1: HOME PAGE SLIDER ---
let currentSlide = 0;
const slides = document.querySelectorAll(".slide");
const totalSlides = slides.length;

function showSlide(index) {
    // Only run if slides exist (avoids errors on other pages)
    if (slides.length === 0) return; 

    slides.forEach((slide) => {
        slide.classList.remove("active");
    });

    if (index >= totalSlides) {
        currentSlide = 0;
    } else if (index < 0) {
        currentSlide = totalSlides - 1;
    } else {
        currentSlide = index;
    }

    slides[currentSlide].classList.add("active");
}

function changeSlide(direction) {
    showSlide(currentSlide + direction);
}

// Auto-play Slider (Every 5 seconds)
if (slides.length > 0) {
    setInterval(() => {
        changeSlide(1);
    }, 5000);
}


// --- PART 2: REGISTERED ALUMNI FILTER ---
function filterTable() {
    // Get values from input and dropdown
    let input = document.getElementById("searchInput");
    let batchFilter = document.getElementById("batchSelect");
    let table = document.getElementById("alumniTable");

    // Exit if elements don't exist (e.g., on Home Page)
    if (!input || !batchFilter || !table) return;

    let filterValue = input.value.toUpperCase();
    let batchValue = batchFilter.value;
    let tr = table.getElementsByTagName("tr");

    // Loop through all table rows (starting from 1 to skip Header)
    for (let i = 1; i < tr.length; i++) {
        let tdName = tr[i].getElementsByTagName("td")[0]; // Name Column
        let tdCourse = tr[i].getElementsByTagName("td")[1]; // Course Column
        let tdBatch = tr[i].getElementsByTagName("td")[2]; // Batch Column
        
        if (tdName && tdBatch) {
            let nameText = tdName.textContent || tdName.innerText;
            let courseText = tdCourse.textContent || tdCourse.innerText;
            let batchText = tdBatch.textContent || tdBatch.innerText;

            // Logic: Does the Name/Course match search? AND Does Batch match dropdown?
            let matchesSearch = nameText.toUpperCase().indexOf(filterValue) > -1 || courseText.toUpperCase().indexOf(filterValue) > -1;
            let matchesBatch = (batchValue === "all" || batchValue === "") ? true : (batchText === batchValue);

            if (matchesSearch && matchesBatch) {
                tr[i].style.display = ""; // Show
            } else {
                tr[i].style.display = "none"; // Hide
            }
        }       
    }
}

/* --- GALLERY LIGHTBOX FUNCTIONALITY --- */

// 1. Define the Images for each Event
// You must list the actual filenames you put in your folders here!
const galleryData = {
    'meet2024': [
        'images/gallery/meet2024/1.jpg',
        'images/gallery/meet2024/2.jpg',
        'images/gallery/meet2024/3.jpg',
        'images/gallery/meet2024/4.jpg',
        'images/gallery/meet2024/5.jpg',
        'images/gallery/meet2024/6.jpg'
    ],
    'meet2023': [
      'images/gallery/meet2024/1.jpg',
        'images/gallery/meet2024/2.jpg',
        'images/gallery/meet2024/3.jpg',
        'images/gallery/meet2024/4.jpg',
        'images/gallery/meet2024/5.jpg',
        'images/gallery/meet2024/6.jpg'
    ],
    'jubilee': [
        'images/gallery/meet2024/1.jpg',
        'images/gallery/meet2024/2.jpg',
        'images/gallery/meet2024/3.jpg',
        'images/gallery/meet2024/4.jpg',
        'images/gallery/meet2024/5.jpg',
        'images/gallery/meet2024/6.jpg'
    ],
    'convcationpics': [
        'images/gallery/meet2024/1.jpg',
        'images/gallery/meet2024/2.jpg',
        'images/gallery/meet2024/3.jpg',
        'images/gallery/meet2024/4.jpg',
        'images/gallery/meet2024/5.jpg',
        'images/gallery/meet2024/6.jpg'
    ]
};

let currentEventImages = []; // Stores the list of images for the clicked event
let currentImageIndex = 0;   // Keeps track of which photo is showing

// Function to Open the Modal
function openGallery(eventID) {
    // Get the list of images for the clicked event
    currentEventImages = galleryData[eventID];

    // Check if images exist for this event
    if (currentEventImages && currentEventImages.length > 0) {
        currentImageIndex = 0; // Reset to first image
        
        // Show the modal
        const modal = document.getElementById('galleryModal');
        const modalImg = document.getElementById('lightboxImg');
        const caption = document.getElementById('caption');
        
        modal.style.display = "flex";
        
        // Load the first image
        // NOTE: If you haven't added real images yet, this might show a broken icon.
        // For now, I will force a placeholder if the file doesn't exist just for demo:
        modalImg.src = currentEventImages[0]; 
        // --------------------------------------

        caption.innerHTML = "Image 1 of " + currentEventImages.length;
    } else {
        alert("No photos uploaded for this event yet!");
    }
}

// Function to Close the Modal
function closeGallery() {
    document.getElementById('galleryModal').style.display = "none";
}

// Function to Change Image (Next/Prev)
function changeGalleryImage(direction) {
    // Update Index
    currentImageIndex += direction;

    // Loop logic (if at end, go to start; if at start, go to end)
    if (currentImageIndex >= currentEventImages.length) {
        currentImageIndex = 0;
    } else if (currentImageIndex < 0) {
        currentImageIndex = currentEventImages.length - 1;
    }

    // Update Image Source
    const modalImg = document.getElementById('lightboxImg');
    const caption = document.getElementById('caption');

    // modalImg.src = currentEventImages[currentImageIndex]; <--- Use this when you have real photos
    modalImg.src = currentEventImages[currentImageIndex];

    caption.innerHTML = "Image " + (currentImageIndex + 1) + " of " + currentEventImages.length;
}
/* --- ADVANCED INFINITE SCROLL LOGIC --- */

function setupInfiniteScroll(trackId, speed = 30) {
    const track = document.getElementById(trackId);
    if (!track) return; // Safety check

    // 1. Ensure images are loaded before calculating width
    // (Images load hone se width badal sakti hai)
    window.addEventListener('load', () => {
        initializeScroll(track, speed);
    });
    
    // Agar window resize ho, toh dobara calculate karein
    window.addEventListener('resize', () => {
        // Reset karke dobara chalayenge
        track.style.animation = 'none';
        track.innerHTML = track.innerHTML.substring(0, track.innerHTML.length / 2); // Remove duplicate
        initializeScroll(track, speed);
    });
}

function initializeScroll(track, speed) {
    // A. Calculate exact width of ORIGINAL content (including gaps)
    // Hum 'gap' ki value nikal kar jodte hain taaki calculation perfect ho
    const gap = parseInt(window.getComputedStyle(track).gap || 0);
    let originalWidth = 0;
    Array.from(track.children).forEach(child => {
        originalWidth += child.offsetWidth + gap;
    });
    
    // Thoda buffer minus karein last gap ke liye
    originalWidth -= gap;

    // B. Duplicate Content
    track.innerHTML += track.innerHTML; 

    // C. Set the CSS Variable for exact scrolling distance
    // Jitni original width thi, utna hi negative mein move karna hai
    track.style.setProperty('--scroll-width', `-${originalWidth}px`);

    // D. Apply Animation
    // 'forwards' ensure karta hai ki jhatka na lage reset par
    track.style.animation = `scrollLeft ${speed}s linear infinite forwards`;
}


// Page load hone par run karein
document.addEventListener("DOMContentLoaded", () => {
    // Testimonials (Speed 35s)
    setupInfiniteScroll('testimonialTrack', 35);
    
    // Events (Speed 45s - thoda slow)
    setupInfiniteScroll('eventTrack', 45);
});