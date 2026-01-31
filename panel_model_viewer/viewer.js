export function render({ model, el }) {
    const viewer = document.createElement("model-viewer");
    viewer.style.display = "block";
    viewer.style.width = "100%";
    viewer.style.height = "100%";

    // Bind attributes
    viewer.alt = model.alt;
    if (model.src) viewer.setAttribute("src", model.src);
    if (model.poster) viewer.setAttribute("poster", model.poster);

    if (model.auto_rotate) viewer.setAttribute("auto-rotate", "");
    if (model.camera_controls) viewer.setAttribute("camera-controls", "");

    // Apply usage css
    for (const [key, value] of Object.entries(model.style)) {
        viewer.style[key] = value;
    }

    // Apply HTML attributes
    for (const [key, value] of Object.entries(model.html_attrs)) {
        viewer.setAttribute(key, value);
    }

    el.appendChild(viewer);

    // Model <-> View Syncing
    // Observe changes from Python
    model.on('src', () => {
        if (model.src) viewer.setAttribute("src", model.src);
        else viewer.removeAttribute("src");
    });
    model.on('alt', () => { viewer.alt = model.alt; });
    model.on('auto_rotate', () => {
        if (model.auto_rotate) viewer.setAttribute("auto-rotate", "");
        else viewer.removeAttribute("auto-rotate");
    });
    model.on('camera_controls', () => {
        if (model.camera_controls) viewer.setAttribute("camera-controls", "");
        else viewer.removeAttribute("camera-controls");
    });
    model.on('poster', () => {
        if (model.poster) viewer.setAttribute("poster", model.poster);
        else viewer.removeAttribute("poster");
    });
    model.on('style', () => {
        for (const [key, value] of Object.entries(model.style)) {
            viewer.style[key] = value;
        }
    });

    // Events back to Python
    viewer.addEventListener('camera-change', (event) => {
        // Example: throttle this if exposing camera state
    });


    viewer.addEventListener('click', (event) => {
        model.send_event('click', {
            clientX: event.clientX,
            clientY: event.clientY,
            target: event.target.tagName
        });
    });

    viewer.addEventListener('error', (event) => {
        console.error("ModelViewer error:", event.detail);
    });
}
