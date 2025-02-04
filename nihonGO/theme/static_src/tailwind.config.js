/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {
            colors: {
                'black': '#181113',
                'white': '#F6F3F4',
                'crimson': '#BD002C',
                'peach': '#F1CD9D',
                'orange': '#E28140',
                'transparent': 'transparent',
            },
            fontFamily : {
                outfit: ['Outfit', 'sans-serif'],
                DMSans: ['DM Sans', 'sans-serif'],
                japanese: ['Noto Sans Japanese', 'sans-serif'],
            },
            fontSize: {
                'title': '100px',
                'heading': '50px',
                'md': '32px',
                'body': '20px',
                'sm': '14px',
            },
            screens: {
                '3xl': '1900px',
            },
            animation: {
                'slide-in-out': 'slideInOut 4s ease-in-out forwards'
            },
            keyframes: {
                slideInOut: {
                    '0%': { transform: 'translateX(100%)', opacity: '0' },
                    '10%': { transform: 'translateX(0)', opacity: '1' },
                    '90%': { transform: 'translateX(0)', opacity: '1' },
                    '100%': { transform: 'translateX(100%)', opacity: '0' },
                },
            }
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
