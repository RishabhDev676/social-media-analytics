import subprocess
import sys
import os


def run_command(command):
    """
    Run a command and stop if an error occurs.
    """

    print("\nRunning:", " ".join(command))

    result = subprocess.run(
        command,
        check=True
    )

    return result


def main():

    # Get project root directory
    project_root = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    src_folder = os.path.join(
        project_root,
        "src"
    )

    requirements_file = os.path.join(
        project_root,
        "requirements.txt"
    )

    print("=" * 50)
    print("SOCIAL MEDIA SENTIMENT ANALYSIS")
    print("=" * 50)

    # ==================================================
    # STEP 1: INSTALL DEPENDENCIES
    # ==================================================

    print("\n[1/4] Installing dependencies...")

    run_command([
        sys.executable,
        "-m",
        "pip",
        "install",
        "-r",
        requirements_file
    ])

    # ==================================================
    # STEP 2: TRAIN MODEL
    # ==================================================

    print("\n[2/4] Training Machine Learning model...")

    run_command([
        sys.executable,
        os.path.join(
            src_folder,
            "train_model.py"
        )
    ])

    # ==================================================
    # STEP 3: RUN PREDICTIONS
    # ==================================================

    print("\n[3/4] Running predictions...")

    run_command([
        sys.executable,
        os.path.join(
            src_folder,
            "predict.py"
        )
    ])

    # ==================================================
    # STEP 4: LAUNCH GUI
    # ==================================================

    print("\n[4/4] Launching GUI...")

    run_command([
        sys.executable,
        os.path.join(
            src_folder,
            "gui.py"
        )
    ])


if __name__ == "__main__":

    try:

        main()

    except subprocess.CalledProcessError as e:

        print("\nERROR:")
        print("A step failed.")

        print(
            "Please check the error above."
        )

        input(
            "\nPress Enter to exit..."
        )