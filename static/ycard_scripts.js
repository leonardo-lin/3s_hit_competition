function toggleYellowBoxes(className) {
    const yellowBoxes = document.querySelectorAll(`.${className} .yellow-box`);
    let visibleCount = Array.from(yellowBoxes).filter(box => box.style.visibility === 'visible').length;

    if (visibleCount < yellowBoxes.length) {
        yellowBoxes[visibleCount].style.visibility = 'visible';
    } else {
        yellowBoxes.forEach(box => box.style.visibility = 'hidden');
    }
}